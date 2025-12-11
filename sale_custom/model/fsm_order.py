from odoo import fields, models


class FSMOrder(models.Model):
    _inherit = "fsm.order"

    sale_order_id = fields.Many2one("sale.order", string="Sales Order")
    sale_line_ids = fields.One2many("sale.product.line", "fsm_order_id", string="Sale Product Lines")


class SaleProductLine(models.Model):
    _name = 'sale.product.line'
    _description = 'Sale Product Line'

    
    fsm_order_id = fields.Many2one('fsm.order', 'Field Service Order')
    product_id = fields.Many2one('product.product', 'Product')
    quantity = fields.Float('Quantity')

