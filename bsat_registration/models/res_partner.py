# bsat_registration/models/res_partner.py
from odoo import models, fields


class ResPartner(models.Model):
    _inherit = "res.partner"

    fathers_name = fields.Char(string="Father's Name")
    whatsapp_number = fields.Char(string="WhatsApp Number")
    registration_date = fields.Date("Registration Date")
    aadhar_number = fields.Char(string="Aadhar Number")
    class_10th_per = fields.Float(string="Class 10th Percentage")
    class_10th_school = fields.Text(string="Class 10th School")
    class_12th_status = fields.Selection([
        ("appearing", "Appearing"),
        ("passed", "Passed")
    ], string="Class 12th Status", default="appearing")
    class_12th_passing_year = fields.Selection([
        ("2023", "2023"),
        ("2024", "2024"),
        ("2025", "2025")
    ], string="12th Passing Year", default="2024")
    class_12th_per = fields.Float(string="Class 12th Percentage")
    class_12th_roll = fields.Char(string="Class 12th Roll No.")
    class_12th_school = fields.Char(string="Class 12th School")
    class_12th_stream = fields.Selection([
        ("pcb", "PCB"),
        ("pcm", "PCM"),
        ("pcmb", "PCMB"),
        ("arts", "Arts"),
        ("commerce", "Commerce"),
        ("others", "Others")
    ], string="12th Stream", default="pcb")
    contact_type = fields.Selection([
        ("student", "Student"),
        ("internal", "Internal"),
        ("other", "Other")
    ], string="Contact Type", default="student")
    registration_token = fields.Char(string="Registration Token")
