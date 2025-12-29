{
    'name': 'SOMDMI Reports',
    'version': '1.0',
    'category': 'Reporting',
    'summary': 'Custom report layouts for SOMDMI',
    'depends': ['web', 'algerian_accounting', 'sale', 'account'],
    'data': [
        'data/ir_config_parameter.xml',
        'data/account_journal_data.xml',
        'views/report_templates.xml',
        'views/account_move_views.xml',
        'views/sale_order_views.xml',
    ],
    'installable': True,
    'application': True,
}
