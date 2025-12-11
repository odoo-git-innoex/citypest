from odoo import fields, models, api


class AccessManagement(models.Model):
    _name = "access.management"
    _description = "Access Management"

    name = fields.Char("Name")
    user_ids = fields.Many2many(
        "res.users",
        "access_management_users_rel_ah",
        "access_management_id",
        "user_id",
        "Users",
    )

    active = fields.Boolean("Active", default=True)
    hide_menu_ids = fields.Many2many(
        "ir.ui.menu",
        "access_management_menu_rel_ah",
        "access_management_id",
        "menu_id",
        "Hide Menu",
    )
    show_menu_ids = fields.Many2many(
        "ir.ui.menu",
        "access_management_show_menu_rel_ah",
        "access_management_id",
        "menu_id",
        "Show Menu",
        compute="_compute_show_menu_ids",
    )
    recursive_show_menu = fields.Boolean("Include Sub-Menus", default=False)
    hide_field_ids = fields.One2many(
        "hide.field", "access_management_id", "Hide Field", copy=True
    )

    remove_action_ids = fields.One2many(
        "remove.action", "access_management_id", "Remove Action", copy=True
    )
    self_model_ids = fields.Many2many(
        "ir.model",
        "access_management_ir_model_self",
        "access_management_id",
        "model_id",
        "Self Model",
        compute="_compute_get_self_module_info",
    )
    total_rules = fields.Integer("Access Rules", compute="_compute_count_total_rules")

    company_ids = fields.Many2many(
        "res.company",
        "access_management_comapnay_rel",
        "access_management_id",
        "company_id",
        "Companies",
        required=True,
        default=lambda self: self.env.company,
    )
    set_show_menu_ids = fields.Many2many("ir.ui.menu", string="Set Show Menu", domain=[("parent_id", "=", False)])
    

    def _compute_count_total_rules(self):
        for rec in self:
            rule = 0
            rule = (
                rule
                + len(rec.hide_menu_ids)
                + len(rec.show_menu_ids)
                + len(rec.hide_field_ids)
                + len(rec.remove_action_ids)
            )
            rec.total_rules = rule

    def action_show_rules(self):
        pass

    def _compute_get_self_module_info(self):
        model_list = [
            "access.management",
            "action.data",
            "hide.field",
            "remove.action",
        ]
        models_ids = self.env["ir.model"].search([("model", "in", model_list)])
        for rec in self:
            rec.self_model_ids = False
            if models_ids:
                rec.self_model_ids = [(6, 0, models_ids.ids)]

    def toggle_active_value(self):
        for record in self:
            record.write({"active": not record.active})
        return True

    @api.depends("set_show_menu_ids")
    def _compute_show_menu_ids(self):
        for rec in self:
            menu_ids = []
            for name in rec.set_show_menu_ids.mapped('display_name'):
                menu_ids += self.env['ir.ui.menu'].search([]).filtered(lambda l: name in l.display_name).ids
            if menu_ids:
                rec.show_menu_ids = [(6, 0, menu_ids)]
            else:
                rec.show_menu_ids = [(5, 0, 0)]

    def remove_show_menu(self):
        for rec in self:
            rec.set_show_menu_ids = [(5, 0, 0)]