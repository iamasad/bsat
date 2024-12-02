from odoo import http, fields
from odoo.http import request
import random
import string
import json

class StudentRegistrationController(http.Controller):

    @http.route('/submit_registration', type='json', auth="public", methods=['POST'], csrf=False)
    def submit_registration(self):
        post = request.httprequest.get_json()

        # Initialize response variables
        message = ""
        status = "error"
        code = 400  # Default to 400 in case of error

        # Check if the post data exists
        if not post:
            message = "No data received"
        else:
            # Check for existing user by mobile or email
            existing_partner = request.env['res.partner'].sudo().search(
                ['|', ('mobile', '=', post.get('mobile')), ('email', '=', post.get('email'))], limit=1
            )
            if existing_partner:
                message = "User already exists."
                status = "duplicate"
                code = 200
            else:
                # Generate a random 10-character registration token
                registration_token = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

                # State searching
                state = request.env['res.country.state'].sudo().search([('name', '=', post.get('state_name'))], limit=1)

                # Create the student record
                partner_data = {
                    'name': post.get('name'),
                    'email': post.get('email'),
                    'mobile': post.get('mobile'),
                    'street': post.get('street'),
                    'city': post.get('city'),
                    'state_id': state.id if state else False,
                    'country_id': request.env.ref('base.in').id,
                    'zip': post.get('zip'),
                    'fathers_name': post.get('fathers_name'),
                    'whatsapp_number': post.get('whatsapp_number'),
                    'registration_date': fields.Date.today(),
                    'aadhar_number': post.get('aadhar_number'),
                    'class_10th_per': post.get('class_10th_per'),
                    'class_10th_school': post.get('class_10th_school'),
                    'class_12th_status': post.get('class_12th_status'),
                    'class_12th_passing_year': post.get('class_12th_passing_year'),
                    'class_12th_per': post.get('class_12th_per'),
                    'class_12th_roll': post.get('class_12th_roll'),
                    'class_12th_school': post.get('class_12th_school'),
                    'class_12th_stream': post.get('class_12th_stream'),
                    'contact_type': 'student',
                    'registration_token': registration_token,
                    'company_type': 'person'
                }

                new_partner = request.env['res.partner'].sudo().create(partner_data)

                # Update response message
                message = "Registration successful!"
                status = "success"
                code = 200

        # Return the response
        response = {
            "message": message,
            "status": status
        }

        return request.make_response(
            json.dumps(response),
            headers={'Content-Type': 'application/json'},
            status=code
        )
