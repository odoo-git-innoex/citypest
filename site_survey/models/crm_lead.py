from odoo import models, fields

class CrmLead(models.Model):
    _inherit = "crm.lead"

    survey_count = fields.Integer(string="Site Surveys", compute="_compute_survey_count")
    is_site_survey = fields.Boolean(string="Is Site Survey", related="stage_id.is_site_survey")
    is_survey_submit = fields.Boolean(string="Is Survey Submit", related="stage_id.is_survey_submit")
    is_new = fields.Boolean(string="Is New", related="stage_id.is_new")
    

    def _compute_survey_count(self):
        for lead in self:
            lead.survey_count = self.env['site.survey'].search_count([('crm_lead_id', '=', lead.id)])

    def action_site_survey(self):
        self.ensure_one()
        stage_id = self.env['crm.stage'].search([('is_site_survey','=',True)], limit=1)
        self.stage_id = stage_id.id
        group = self.env.ref('sales_team.group_sale_manager')
        activity_type = self.env.ref('mail.mail_activity_data_todo')
        for user in group.users:
            self.activity_schedule(
                activity_type_id=activity_type.id,
                summary='Site Survey Initiated',
                note=f'Site survey has been scheduled for {self.name}',
                user_id=user.id
            )
        
        return True
        

    def create_site_survey(self):
        self.ensure_one()
        action = self.env["ir.actions.act_window"]._for_xml_id("site_survey.action_site_survey")
        action.update({
            'view_mode': 'form',
            'views': [(self.env.ref('site_survey.view_site_survey_form').id, 'form')],
            'target': 'current',
            'context': {
                'default_customer_name': self.partner_id.name if hasattr(self, 'partner_id') else "",
                'default_crm_lead_id': self.id,
                'default_location_id': self.fsm_location_id.id,
                'default_company_id': self.company_id.id
            }
        })
        return action
    
    def action_view_site_survey(self):
        self.ensure_one()
        action = self.env["ir.actions.act_window"]._for_xml_id("site_survey.action_site_survey")
        action['domain'] = [('crm_lead_id', '=', self.id)]
        return action
    

    def write(self, vals):
        res = super(CrmLead, self).write(vals)
        stage_id = self.env['crm.stage'].search([('is_site_survey','=',True)], limit=1)
        if 'stage_id' in vals:
            if self.stage_id.id == stage_id.id:
                group = self.env.ref('sales_team.group_sale_manager')
                activity_type = self.env.ref('mail.mail_activity_data_todo')
                for user in group.users:
                    self.activity_schedule(
                        activity_type_id=activity_type.id,
                        summary='Site Survey Initiated',
                        note=f'Site survey has been scheduled for {self.name}',
                        user_id=user.id
                    )
        return res
