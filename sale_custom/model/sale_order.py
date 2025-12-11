from odoo import models, fields, _
from odoo.exceptions import UserError


SALE_ORDER_STATE = [
    ('draft', "Quotation"),
    ('sent', "Quotation Sent"),
    ('add_lpo_contract', 'Add LPO/Contract'),
    ('sale', "Sales Order"),
    ('cancel', "Cancelled"),
]

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    document_choice = fields.Selection([('add_lpo', 'Add LPO'),
                                        ('add_contract', 'Add Contract'), 
                                        ('nothing', 'Nothing')], string="Document Choice", default=False)
    
    lpo_number = fields.Char(string="L.P.O. No.")
    lpo_doc_ids = fields.Many2many("ir.attachment", relation="sale_order_lpo_rel", string='LPO Document')

    contract_doc_ids = fields.Many2many("ir.attachment", relation="sale_order_contract_rel", string='Contract Document')

    fsm_order_ids = fields.One2many(
        "fsm.order", "sale_order_id", string="Service Orders"
    )
    fsm_order_count = fields.Integer(
        compute="_compute_fsm_order_count", string="# FSM Orders"
    )

    def _compute_fsm_order_count(self):
        for rec in self:
            rec.fsm_order_count = len(rec.fsm_order_ids)

    def action_create_fsm_order(self):
        self.ensure_one()
        if not self.partner_id:
            raise UserError(_("Please select a customer."))
        
        location_id = self.partner_shipping_id.fsm_location_id or self.partner_id.fsm_location_id
        if not location_id:
             if not self.partner_id.fsm_location:
                self.env["fsm.wizard"].action_convert_location(self.partner_id)
             location_id = self.partner_id.fsm_location_id


        return {
            "name": _("Create FSM Order"),
            "type": "ir.actions.act_window",
            "res_model": "fsm.order",
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_sale_order_id": self.id,
                "default_lead_id": self.opportunity_id.id if self.opportunity_id else False,
                "default_opportunity_id": self.opportunity_id.id if self.opportunity_id else False,
                "default_location_id": location_id.id,
                "default_sale_line_ids": [(0,0, {'product_id':i.product_id.id, 'quantity': i.product_uom_qty}) for i in self.order_line]
            },
        }

    def action_view_fsm_orders(self):
        self.ensure_one()
        action = self.env.ref("fieldservice.action_fsm_dash_order").read()[0]
        action["domain"] = [("sale_order_id", "=", self.id)]
        action["context"] = {
            "default_sale_order_id": self.id,
            "default_opportunity_id": self.opportunity_id.id if self.opportunity_id else False,
        }
        return action



    state = fields.Selection(
        selection=SALE_ORDER_STATE,
        string="Status",
        readonly=True, copy=False, index=True,
        tracking=3,
        default='draft')

    sub = fields.Char(
        string='Sub',
        default='Quotation for Annual Pest Control Service in DBB Bulgarie Light House Project AD9317 @ Jumerian Bay'
    )
    ref = fields.Char(
        string='Ref',
        default='The Survey we made today.'
    )

    def action_confirm(self):
        if self.state in ['sent', 'draft']:
            if self.document_choice != 'nothing':
                needs_lpo_check = self.document_choice == 'add_lpo' and not (self.lpo_number and self.lpo_doc_ids)
                needs_contract_check = self.document_choice == 'add_contract' and not self.contract_doc_ids
                
                if needs_lpo_check or needs_contract_check:
                    self.state = 'add_lpo_contract'
                    return True
        else:
            if self.state == 'add_lpo_contract':
                self.state = 'sent'
        return super(SaleOrder, self).action_confirm()
    
    
    def _prepare_invoice(self):
        """Override."""
        res = super()._prepare_invoice()
        if self.lpo_number:
            res["lpo_number"] = self.lpo_number
        return res


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    fsm_order_id = fields.Many2one("fsm.order", string="FSM Order")

