from odoo import api, fields, models


class FieldServicePestType(models.Model):
    _name = 'field.service.pest.type'
    _description = 'Pest Types'

    name = fields.Char(required=True)


class FieldServiceReport(models.Model):
    _name = 'field.service.report'
    _description = 'Field Service Report'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'service_date desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    lead_id = fields.Many2one('crm.lead', string='Lead', required=True, tracking=True)
    sale_order_id = fields.Many2one('sale.order', string='Service Order', tracking=True)
    service_date = fields.Date(string='Date of Service', required=True, default=fields.Date.today, tracking=True)
    technician_id = fields.Many2one('res.users', string='Supervisor Name', tracking=True,
                                    default=lambda self: self.env.user.id if self.env.user else False)
    report_details = fields.Html(string='Description of Services')
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company, tracking=True)
    # customer_name = fields.Char(string='Customer Name', compute='_compute_customer_name', store=True, readonly=True)
    customer_id = fields.Many2one('res.partner', string='Customer Name', store=True)
    targeted_pest_ids = fields.Many2many('field.service.pest.type', string='Targeted Pests', tracking=True)
    targeted_pest_other = fields.Char(string='Targeted Pest (Other)', tracking=True)

    type_of_visit = fields.Selection([
        ('major', 'Major'),
        ('one_time', 'One Time'),
        ('call_out', 'Call Out'),
        ('inspection', 'Inspection'),
        ('follow_up', 'Follow-Up'),
        ('routine_job', 'Routine Job'),
        ('others', 'Others (Specify)'),
    ], string='Type of Visit', tracking=True)
    type_of_visit_other = fields.Char(string='Type of Visit (Other)', tracking=True)

    recommendations_remarks = fields.Html(string='Recommendations/Remarks')

    # Client Approval Signature Section
    client_signature = fields.Binary(string='Client Signature', help='Digital signature of the client')
    client_signature_filename = fields.Char(string='Signature Filename')
    client_approval_date = fields.Date(string='Approval Date', help='Date when client approved the service')
    client_approver_name = fields.Char(string='Client Name', help='Name of the person who approved the service')
    client_approver_title = fields.Char(string='Client Title/Position', help='Title or position of the approver')

    field_service_order_id = fields.Many2one('fsm.order', string='Field Service Order', readonly=True, tracking=True)
    location_id = fields.Many2one('fsm.location', string='Location', tracking=True)
    show_targeted_pest_other = fields.Boolean(
        string='Show Targeted Pest Other',
        compute='_compute_show_targeted_pest_other',
        store=False
    )

    # Lines from related Sales Order and FSM Order (read-only views)
    chemical_used_ids = fields.One2many(
        'fs.report.chemical.used',
        'field_service_report_id',
        string='Chemical Used',
    )
    products_used = fields.One2many(
        related='sale_order_id.order_line',
        string='Products Used (Sales Order)',
        readonly=True
    )

    fsm_products_used = fields.One2many(
        related='field_service_order_id.product_line_ids',
        string='Additional Services (FSM Order)',
        readonly=False
    )

    time_from = fields.Float(string='Time From', default=0.0)
    time_to = fields.Float(string='Time To', default=0.0)
    building_type = fields.Selection([
                                        ('residential', 'Residential'),
                                        ('commercial', 'Commercial'),
                                        ('industrial', 'Industrial'),
                                    ], string="Building Type", required=True)
    building_space = fields.Text(string="Building Space/Side")
    entry_points_observation = fields.Html(string="Entry Points Observation")
    followup_recommendation_ids = fields.Many2many('followup.recommendation', string='Followup Recommendation')
    method_application_id = fields.Many2one('method.application', string='Method Application')
    field_service_order_id = fields.Many2one('fsm.order', string='Field Service Order', index=True)
    

    @api.depends('targeted_pest_ids')
    def _compute_show_targeted_pest_other(self):
        for record in self:
            record.show_targeted_pest_other = any(pest.name == 'Others' for pest in record.targeted_pest_ids)

    
    def get_recommendation(self):
        return self.recommendations_remarks
    
    @api.onchange('lead_id')
    def _onchange_lead_id(self):
        if self.lead_id:
            orders = self.env['sale.order'].search([
                ('opportunity_id', '=', self.lead_id.id),
                ('state', 'in', ['sale', 'done'])
            ], order='date_order desc', limit=1)
            if orders:
                self.sale_order_id = orders.id

    @api.onchange('lead_id', 'sale_order_id', 'technician_id', 'company_id')
    def _onchange_many2one_fields(self):
        if self.lead_id and not self.lead_id.exists():
            self.lead_id = False
        if self.sale_order_id and not self.sale_order_id.exists():
            self.sale_order_id = False
        if self.technician_id and not self.technician_id.exists():
            self.technician_id = False
        if self.company_id and not self.company_id.exists():
            self.company_id = self.env.company

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('field.service.report') or 'New'
        return super().create(vals_list)

    def action_send_email(self):
        self.ensure_one()
        template = self.env.ref('fs_service_report.email_template_field_service_report')
        if not template:
            raise ValueError("Email template not found.")
        if not self.lead_id.partner_id or not self.lead_id.partner_id.email:
            raise ValueError("No valid email address found for the customer.")
        email_values = {
            'email_from': self.company_id.email_formatted or self.env.user.email_formatted or 'no-reply@demopest.velvetbud.in',
            # 'attachment_ids': [(0, 0, {
            #     'name': f"Field_Service_Report_{self.name}.pdf",
            #     'datas':
            #         self.env['ir.actions.report']._render_qweb_pdf('fs_service_report.service_template_id',
            #                                                        self.id)[0],
            #     'mimetype': 'application/pdf',
            # })],
        }
        template.send_mail(self.id, force_send=True, email_values=email_values)
        self.message_post(body="Service Report sent to %s" % (self.lead_id.partner_id.name or 'Customer'))
