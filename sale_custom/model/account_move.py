from odoo import models, fields

class AccountMove(models.Model):
    _inherit = "account.move"

    do_number = fields.Char(string="D.O. No.")
    lpo_number = fields.Char(string="L.P.O. No.")
