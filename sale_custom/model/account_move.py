from odoo import models, fields

class AccountMove(models.Model):
    _inherit = "account.move"

    do_number = fields.Char(string="D.O. No.", compute="_compute_do_number", readonly=False)
    lpo_number = fields.Char(string="L.P.O. No.")
    service_date = fields.Datetime('Service Date')

    def _compute_do_number(self):
        for record in self:
            do_number = ''
            sale_order = record.invoice_line_ids.sale_line_ids.order_id
            fieldservice = sale_order.fsm_order_ids
            if fieldservice:
                servic_report = self.env['field.service.report'].search([('field_service_order_id', '=', fieldservice[0].id)], limit=1)
                do_number = servic_report.name or fieldservice[0].name
            record.do_number = do_number

