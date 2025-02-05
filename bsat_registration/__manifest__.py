# bsat_registration/__manifest__.py
{
    'name': 'BSAT Registration',
    'version': '18.0.0.1',
    'category': 'Custom',
    'author': 'Md Asadullah',
    'depends': ['base','contacts'],
    'data': [
        'views/res_partner.xml',
    ],
    'application': True,
    'license': 'LGPL-3'
}
