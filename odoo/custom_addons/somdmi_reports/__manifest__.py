{
    'name': 'SOMDMI Reports',
    'version': '1.0',
    'category': 'Reporting',
    'summary': 'Custom report layouts for SOMDMI',
    'depends': ['web', 'algerian_accounting', 'sale', 'account'],
    'data': [
        'data/ir_config_parameter.xml',
        'views/report_templates.xml',
    ],
    'installable': True,
    'application': True,
}
