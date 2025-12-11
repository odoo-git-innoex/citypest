from odoo import models, fields 


class SiteSurveyPest(models.Model):
    _name = "site.survey.pest"
    _description = "Survey Pests"

    name = fields.Char(string="Pest Name", required=True)