from odoo import fields, models


class RemoveAction(models.Model):
    _name = "remove.action"
    _description = "Models Right"

    access_management_id = fields.Many2one("access.management", "Access Management")
    model_id = fields.Many2one("ir.model", "Model")
    server_action_ids = fields.Many2many(
        "action.data",
        "remove_action_server_action_data_rel_ah",
        "remove_action_id",
        "server_action_id",
        "Hide Actions",
        domain="[('action_id.binding_model_id', '=', model_id), ('action_id.type', '!=', 'ir.actions.report')]",  # noqa
    )
    report_action_ids = fields.Many2many(
        "action.data",
        "remove_action_report_action_data_rel_ah",
        "remove_action_id",
        "report_action_id",
        "Hide Reports",
        domain="[('action_id.binding_model_id', '=', model_id), ('action_id.type', '=', 'ir.actions.report')]",  # noqa
    )
    restrict_create = fields.Boolean("Hide Create")
    restrict_edit = fields.Boolean("Hide Edit")
    restrict_delete = fields.Boolean("Hide Delete")
