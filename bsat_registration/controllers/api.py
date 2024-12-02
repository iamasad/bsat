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

        # Check for existing user by mobile or email
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

        # State searching
        state = request.env['res.country.state'].sudo().search(
            [('name', '=', post.get('state_name'))], limit=1)

        # Create the student record
        partner_data = {
            'name': post.get('name'),
            'email': post.get('email'),
            'mobile': post.get('mobile'),
            'street': post.get('street'),
            'city': post.get('city'),
            'state_id': state and state.id or False,
            # Set country to India
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
            'company_type': 'person'  # Always set to 'person'
        }

        # Create the record
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
