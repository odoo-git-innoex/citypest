from odoo import models, fields, _


class FSMOrderProductLine(models.Model):
    _name = 'fsm.order.product.line'
    _description = 'Products Used in FSM Order'

    order_id = fields.Many2one(
        'fsm.order',
        string='FSM Order',
        required=True,
        ondelete='cascade'
    )
    product_id = fields.Many2one(
        'product.product',
        string='Product',
        required=True
    )
    quantity = fields.Float(
        string='Quantity',
        required=True,
        default=1.0
    )
    product_uom_id = fields.Many2one(
        'uom.uom',
        string='Unit of Measure',
        related='product_id.uom_id',
        readonly=True
    )


class FSMOrder(models.Model):
    _inherit = 'fsm.order'

    product_line_ids = fields.One2many(
        'fsm.order.product.line',
        'order_id',
        string='Products Used'
    )

