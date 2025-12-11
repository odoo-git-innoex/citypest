from odoo import models, fields


class CrmStage(models.Model):
    _inherit = "crm.stage"


    is_site_survey = fields.Boolean(string="Is Site Survey")
    is_survey_submit = fields.Boolean(string="Is Survey Submit")
    is_new = fields.Boolean(string="Is New")
    active = fields.Boolean(string="active", default=True)