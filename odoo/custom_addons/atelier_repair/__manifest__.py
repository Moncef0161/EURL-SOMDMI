# -*- coding: utf-8 -*-
{
    'name': 'Atelier',
    'version': '1.0',
    'category': 'Inventory/Inventory',
    'summary': 'Gestion de l\'Atelier',
    'description': """
Ce module renomme le module de Réparation en Atelier et personnalise ses menus.
""",
    'author': 'Moncef',
    'depends': ['repair', 'algerian_accounting', 'stock', 'contacts', 'purchase_repair'],
    'data': [
        'data/product_category_data.xml',
        'data/stock_location_data.xml',
        'data/ir_sequence_data.xml',
        'data/product_type_data.xml',
        'data/operation_type_data.xml',
        'security/ir.model.access.csv',
        'views/product_views.xml',
        'views/stock_picking_views.xml',
        'report/repair_checklist_report.xml',
        'report/stock_picking_report.xml',
        'views/repair_menus.xml',
        'views/repair_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': True,
    'license': 'LGPL-3',
}
