from odoo import models, api


class IrUiMenu(models.Model):
    _inherit = "ir.ui.menu"

    @api.model
    def search(self, domain, offset=0, limit=None, order=None):
        menus = super().search(domain, offset=offset, limit=limit, order=order)
        menus_ids = menus.ids
        user = self.env.user
        cids = self.env.company.id

        # Logic for Show Menu (Whitelist)
        access_management_ids = self.env['access.management'].search([]).filtered(lambda line: int(user.id) in line.user_ids.ids)

        if access_management_ids:
            show_menu_ids = user.access_management_ids.filtered(
                lambda line: int(cids) in line.company_ids.ids
            ).mapped("show_menu_ids")

            if show_menu_ids:
                # If there are any show menus defined, restrict to ONLY those
                menus_ids = [menu_id for menu_id in menus_ids if menu_id in show_menu_ids.ids]

            # Logic for Hide Menu (Blacklist)
            for menu_id in user.access_management_ids.filtered(
                lambda line: int(cids) in line.company_ids.ids
            ).mapped("hide_menu_ids"):
                if menu_id.id in menus_ids:
                    menus_ids.remove(menu_id.id)
            
            menus = self.browse(menus_ids)
        return menus
