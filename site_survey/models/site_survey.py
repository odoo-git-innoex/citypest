from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import timedelta

class SiteSurvey(models.Model):
    _name = "site.survey"
    _description = "Site Survey"

    name = fields.Char(string="Survey Name", required=True, default="New")
    location_id = fields.Many2one("fsm.location", string="Location", ondelete="cascade")
    crm_lead_id = fields.Many2one("crm.lead", string="CRM Lead", ondelete="set null")
    customer_name = fields.Char(string="Customer Name", readonly=True)
    company_id = fields.Many2one("res.company", string="Company")
    locality_type = fields.Selection([
        ('individual', 'Individual'),
        ('community', 'Community'),
    ], string="Locality Type", required=True)
    building_type = fields.Selection([
        ('residential', 'Residential'),
        ('commercial', 'Commercial'),
        ('industrial', 'Industrial'),
    ], string="Building Type", required=True)
    subcategory = fields.Selection([
        ('flat', 'Flat'),
        ('villa', 'Villa'),
        ('hotel', 'Hotel'),
        ('restaurant', 'Restaurant'),
        ('cafeteria', 'Cafeteria'),
        ('supermarket', 'Supermarket'),
        ('food_factory', 'Food Factory'),
        ('food_warehouse', 'Food Warehouse'),
        ('industrial_warehouse', 'Industrial Warehouse'),
        ('clinic', 'Clinic'),
        ('hospital', 'Hospital'),
        ('mall', 'Mall'),
    ], string="Subcategory")
    flat_people_living = fields.Integer(string="Number of People Living")
    flat_sharing = fields.Selection([
        ('sharing', 'Sharing'),
        ('non_sharing', 'Non-Sharing'),
    ], string="Sharing Type")
    flat_beds = fields.Integer(string="Number of Beds")
    flat_type = fields.Selection([
        ('studio', 'Studio'),
        ('1bhk', '1 BHK'),
        ('2bhk', '2 BHK'),
        ('3bhk', '3 BHK'),
        ('4plus', '4+ BHK'),
    ], string="Flat Type")
    villa_type = fields.Selection([
        ('3bhk', '3 BHK'),
        ('4bhk', '4 BHK'),
        ('5plus', '5+ BHK'),
    ], string="Villa Type")
    commercial_apartments = fields.Integer(string="Number of Apartments")
    commercial_floors = fields.Integer(string="Number of Floors")
    commercial_garbage_rooms = fields.Integer(string="Number of Garbage Rooms")
    commercial_water_tanks = fields.Integer(string="Number of Water Tanks")
    commercial_lifts = fields.Integer(string="Number of Lifts")
    commercial_total_area = fields.Float(string="Total Area (sqm)")
    hotel_rooms = fields.Integer(string="Number of Rooms")
    hotel_kitchens = fields.Integer(string="Number of Kitchens")
    hotel_dining_areas = fields.Integer(string="Number of Dining Areas")
    hotel_dining_type = fields.Selection([
        ('indoor', 'Indoor'),
        ('outdoor', 'Outdoor'),
        ('both', 'Both'),
    ], string="Dining Type")
    mall_outlets = fields.Integer(string="Number of Outlets")
    mall_receiving_areas = fields.Integer(string="Number of Receiving Areas")
    mall_water_tanks = fields.Integer(string="Number of Water Tanks")
    pest_type_ids = fields.Many2many("site.survey.pest", string="Type of Pests")
    no_of_floors = fields.Integer(string="Number of Floors")
    no_of_bedrooms = fields.Integer(string="Number of Bedrooms")
    has_basement = fields.Boolean(string="Basement Present?")
    total_area = fields.Float(string="Total Area (sqm)")
    remarks = fields.Text(string="Remarks")
    pest_reported = fields.Boolean(string="Pest Reported?")
    compliance_status = fields.Selection([
        ('compliant', 'Compliant'),
        ('non_compliant', 'Non-Compliant'),
        ('pending', 'Pending'),
    ], string="Compliance Status")
    pictures = fields.Many2many("ir.attachment", relation="site_survey_pictures_rel", string="Pictures", domain="[('mimetype', 'ilike', 'image')]")
    videos = fields.Many2many("ir.attachment", relation="site_survey_videos_rel", string="Videos", domain="[('mimetype', 'ilike', 'video')]")
    retention_period = fields.Integer(string="Retention Period (days)", default=30)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted')],default='draft', string="State")
    infestation_level = fields.Selection([
        ('low', 'Low'),
        ('moderator', 'Moderator'),
        ('high', 'High'),
    ], string="Infestation Level")
    entry_points_observation = fields.Html(string='Entry Points Observation')

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('site.survey') or 'New'
        return super().create(vals)
    
    def action_submit(self):
        self.crm_lead_id.stage_id = self.env['crm.stage'].search([('is_survey_submit','=',True)], limit=1).id
        self.write({'state': 'submitted'})


