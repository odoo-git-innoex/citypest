from odoo import api, models


class Base(models.AbstractModel):
    _inherit = "base"

    @api.model
    def _get_view(self, view_id=None, view_type="form", **options):
        arch, view = super()._get_view(view_id, view_type, **options)
        hide_field_obj = self.env["hide.field"].sudo()
        for hide_field in hide_field_obj.search(
            [
                ("access_management_id.company_ids", "in", self.env.company.id),
                ("model_id.model", "=", self._name),
                ("access_management_id.active", "=", True),
                ("access_management_id.user_ids", "in", self._uid),
            ]
        ):
            for field_id in hide_field.field_id:
                for node in arch.xpath(f"//field[@name='{field_id.name}']"):
                    if hide_field.invisible:
                        node.attrib["invisible"] = "1"
                    if hide_field.readonly:
                        node.attrib["readonly"] = "1"
                        node.attrib["force_save"] = "1"
                    if hide_field.required:
                        node.attrib["required"] = "1"
        return arch, view
