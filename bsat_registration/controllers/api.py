from odoo import http, fields
from odoo.http import request, Response
import json
import random
import string


class StudentRegistrationController(http.Controller):

    @http.route('/submit_registration', type='json', auth="public", methods=['POST'], cors='*', csrf=False)
    def submit_registration(self):
        post = request.httprequest.get_json()

        # Validate the received data
        if not post:
            return Response(
                json.dumps({"error": "No data received."}),
                status=400,
                mimetype='application/json'
            )

        # Check for required fields
        required_fields = ['name', 'email', 'mobile']
        missing_fields = [
            field for field in required_fields if not post.get(field)]
        if missing_fields:
            return Response(
                json.dumps({"error": f"Missing required fields: {
                           ', '.join(missing_fields)}."}),
                status=400,
                mimetype='application/json'
            )

        # Check for existing user by mobile or email
        existing_partner = request.env['res.partner'].sudo().search(
            ['|', ('mobile', '=', post.get('mobile')), ('email', '=', post.get('email'))], limit=1
        )
        if existing_partner:
            return Response(
                json.dumps(
                    {"error": "A user with this mobile or email already exists. Please check your details."}),
                status=400,
                mimetype='application/json'
            )

        # Generate a random 10-character registration token
        registration_token = ''.join(random.choices(
            string.ascii_uppercase + string.digits, k=10))

        # Search for state
        state = request.env['res.country.state'].sudo().search(
            [('name', '=', post.get('state_name'))], limit=1)

        # Prepare partner data
        partner_data = {
            'name': post.get('name'),
            'email': post.get('email'),
            'mobile': post.get('mobile'),
            'street': post.get('street'),
            'city': post.get('city'),
            'state_id': state.id if state else False,
            # Country set to India
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

        # Create the student record
        new_partner = request.env['res.partner'].sudo().create(partner_data)

        return Response(
            json.dumps({
                "success": True,
                "message": "Registration successful!",
                "registration_token": new_partner.registration_token
            }),
            status=200,
            mimetype='application/json'
        )
