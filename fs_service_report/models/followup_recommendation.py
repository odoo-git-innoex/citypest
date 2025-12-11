from odoo import models, fields

class FollowupRecommendation(models.Model):
    _name = 'followup.recommendation'
    _description = 'Followup Recommendation'
    _rec_name = 'recommendation'

    recommendation = fields.Char(string='Recommendation')