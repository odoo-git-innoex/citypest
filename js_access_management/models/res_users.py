from odoo import fields, models


class ResUsers(models.Model):
    _inherit = "res.users"

    access_management_ids = fields.Many2many(
        "access.management",
        "access_management_users_rel_ah",
        "user_id",
        "access_management_id",
        "Access Pack",
    )
