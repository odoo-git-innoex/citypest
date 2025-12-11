from odoo import models, fields, api, _
from odoo.exceptions import UserError

class FSMOrder(models.Model):
    _inherit = 'fsm.order'

    lead_id = fields.Many2one('crm.lead', string='Lead', tracking=True)
    customer_id = fields.Many2one('res.partner', string='Customer', related="lead_id.partner_id", store=True)
    is_new = fields.Boolean(string="Is New",related="stage_id.is_new")
    is_completed = fields.Boolean(string="Is Completed",related="stage_id.is_completed")
    service_report_count = fields.Integer(string="Service Report Count", compute='_compute_service_report_count')
    method_application_id = fields.Many2one('method.application', string='Method Application')

    def _compute_service_report_count(self):
        for order in self:
            order.service_report_count = self.env['field.service.report'].search_count([('field_service_order_id', '=', order.id)])

    @api.onchange('lead_id')
    def _onchange_lead_id(self):
        if self.lead_id:
            self.customer_id = self.lead_id.partner_id.id or False

    def action_create_service_report(self):
        self.ensure_one()

        # Require Lead before report creation
        if not self.lead_id:
            raise UserError(_("Please select a Lead on the FSM Order before creating the Service Report."))

        report_model = self.env['field.service.report']
        report = report_model.search([('field_service_order_id', '=', self.id)], limit=1)
        if report:
            return {
                'name': 'Service Report',
                'type': 'ir.actions.act_window',
                'res_model': 'field.service.report',
                'res_id': report.id,
                'view_mode': 'form',
                'target': 'current',
            }

        report_vals = {
            'lead_id': self.lead_id.id,
            'customer_id': self.customer_id.id,
            'sale_order_id': getattr(self, 'sale_order_id', False) and self.sale_order_id.id or False,
            'technician_id': getattr(self, 'person_id', False) and self.person_id.user_id.id or False,
            'service_date': fields.Date.context_today(self),
            'field_service_order_id': self.id,
            'report_details': self.description or '',
            'location_id': self.location_id.id if self.location_id else self.customer_id.service_location_id.id,
        }
        report = report_model.create(report_vals)

        return {
            'name': 'Service Report',
            'type': 'ir.actions.act_window',
            'res_model': 'field.service.report',
            'res_id': report.id,
            'view_mode': 'form',
            'target': 'current',
        }

    def action_view_service_report(self):
        self.ensure_one()
        return {
            'name': 'Service Report',
            'type': 'ir.actions.act_window',
            'res_model': 'field.service.report',
            'domain': [('field_service_order_id', '=', self.id)],
            'view_mode': 'tree,form',
            'target': 'current',
        }
