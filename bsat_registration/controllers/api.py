import random
import string
from odoo import http, fields
from odoo.http import request, Response
import json


class StudentRegistrationController(http.Controller):

    @http.route('/submit_registration', type='http', auth="public", methods=['POST'], cors='*', csrf=False)
    def submit_registration(self):
        post = request.httprequest.get_json()

        if not post:
            return Response(
                json.dumps({
                    "status": "error",
                    "message": "No data received"
                }),
                headers=[('Content-Type', 'application/json')],
                status=400  # Bad Request
            )

        # Check for existing user by mobile or email (Optional validation)
        if post.get('mobile') or post.get('email'):
            existing_partner = request.env['res.partner'].sudo().search(
                ['|', ('mobile', '=', post.get('mobile')), ('email', '=', post.get('email'))], limit=1
            )
            if existing_partner:
                return Response(
                    json.dumps({
                        "status": "error",
                        "message": "A user with this mobile or email already exists."
                    }),
                    headers=[('Content-Type', 'application/json')],
                    status=409  # Conflict
                )

        # Generate a random 10-character registration token
        registration_token = ''.join(
            random.choices(string.ascii_uppercase, k=10))

        # State searching (optional, only if 'state_name' is provided)
        state = None
        if post.get('state_name'):
            state = request.env['res.country.state'].sudo().search(
                [('name', '=', post.get('state_name'))], limit=1
            )

        # Prepare partner data with defaults for optional fields
        partner_data = {
            'name': post.get('name', False),
            'email': post.get('email', False),
            'mobile': post.get('mobile', False),
            'street': post.get('street', False),
            'city': post.get('city', False),
            'state_id': state.id if state else False,  # Optional state
            'country_id': request.env.ref('base.in').id,  # Always set to India
            'zip': post.get('zip', False),
            'fathers_name': post.get('fathers_name', False),
            'whatsapp_number': post.get('whatsapp_number', False),
            'registration_date': fields.Date.today(),
            'aadhar_number': post.get('aadhar_number', False),
            'class_10th_per': post.get('class_10th_per', False),
            'class_10th_school': post.get('class_10th_school', False),
            'class_12th_status': post.get('class_12th_status', False),
            'class_12th_passing_year': post.get('class_12th_passing_year', False),
            'class_12th_per': post.get('class_12th_per', False),
            'class_12th_roll': post.get('class_12th_roll', False),
            'class_12th_school': post.get('class_12th_school', False),
            'class_12th_stream': post.get('class_12th_stream', False),
            'contact_type': 'student',  # This remains fixed
            'registration_token': registration_token,
            'company_type': 'person'  # Always set to 'person'
        }

        # Create the partner record
        new_partner = request.env['res.partner'].sudo().create(partner_data)

        # Debug: Print the result to check if the partner was created
        print("New partner created:", new_partner)

        # Return a success message with registration token
        return Response(
            json.dumps({
                "status": "success",
                "message": "Registration successful!",
                "registration_token": new_partner.registration_token
            }),
            headers=[('Content-Type', 'application/json')],
            status=200  # OK
        )
