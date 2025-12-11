from odoo import models, fields


class ChemicalUsed(models.Model):
    _name = 'fs.report.chemical.used'
    _description = 'Chemical Used'

    field_service_report_id = fields.Many2one('field.service.report', string='Field Service Report', required=True)
    product_id = fields.Many2one('product.product', string='Product', required=True)
    product_uom_qty = fields.Float(string='Quantity', required=True)
    remarks = fields.Char(string='Remarks')