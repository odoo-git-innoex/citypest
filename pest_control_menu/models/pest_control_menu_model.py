from odoo import models, fields

class PestControl(models.Model):
    _name = 'pest.control'
    _description = 'Pest Control'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')

