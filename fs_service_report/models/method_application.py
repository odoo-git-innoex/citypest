from odoo import models, fields

class MethodApplication(models.Model):
    _name = 'method.application'
    _description = 'Method Application'
    _rec_name = 'method_application'

    method_application = fields.Char(string='Method Application')