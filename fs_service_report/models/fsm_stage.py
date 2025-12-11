from odoo import _, api, fields, models


class FSMStage(models.Model):
    _inherit = "fsm.stage"
    
    is_new = fields.Boolean(string="Is New")
    is_completed = fields.Boolean(string="Is Completed")