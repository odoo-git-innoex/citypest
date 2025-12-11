from odoo.addons.web.controllers.utils import ensure_db
from odoo.addons.web.controllers.home import Home
from odoo.http import request
from odoo import http


class Home(Home):
    @http.route("/web", type="http", auth="none")
    def web_client(self, s_action=None, **kw):
        ensure_db()
        request.env["ir.ui.view"].clear_caches()
        request.env["ir.qweb"].clear_caches()
        request.env["ir.actions.actions"].clear_caches()
        user = request.env.user.browse(request.session.uid)
        if len(user.company_ids) > 1:
            request.env["ir.ui.menu"].clear_caches()
        return super().web_client(s_action=s_action, **kw)
