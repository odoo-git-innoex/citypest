from odoo import http
from odoo.http import request
import logging

_logger = logging.getLogger(__name__)

class PestControl(http.Controller):
    @http.route('/pest_control/', auth='public', website=True, csrf=True)
    def pest_control_form(self, **kwargs):
        _logger.info("Rendering pest control form")
        return request.render('pest_control.pest_control_form_template', {})

    @http.route('/pest_control/submit', auth='public', website=True, csrf=True, type='http', methods=['POST'])
    def pest_control_submit(self, **post):
        try:
            _logger.info("Received POST data: %s", request.httprequest.form)
            name = post.get('name')
            email = post.get('email')
            phone = post.get('phone')
            description = post.get('description')
            _logger.info("Parsed form data: Name=%s, Email=%s, Phone=%s, Description=%s", name, email, phone, description)

            # Ensure description is valid HTML
            description = f"<p>{description or 'No description provided'}</p>"

            # Create a contact (res.partner) with Customer tag
            partner = request.env['res.partner'].sudo().create({
                'name': name,
                'email': email,
                'phone': phone,
                'is_company': False,
                'category_id': [(4, request.env.ref('pest_control.partner_tag_customer').id)],
            })
            _logger.info("Created partner: ID=%s, Name=%s", partner.id, partner.name)

            # Create the lead and link it to the contact
            lead = request.env['crm.lead'].sudo().create({
                'name': f"{name} - Pest Control Inquiry",
                'partner_id': partner.id,
                'partner_name': name,
                'email_from': email,
                'phone': phone,
                'description': description,
            })
            _logger.info("Lead created: ID=%s, Description=%s", lead.id, lead.description)

            return request.render('pest_control.pest_control_success_template', {'lead': lead})
        except Exception as e:
            _logger.error("Error in form submission: %s", str(e))
            return request.render('pest_control.pest_control_error_template', {'error': str(e)})
