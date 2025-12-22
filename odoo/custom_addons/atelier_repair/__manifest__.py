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
    'depends': ['repair'],
    'data': [
        'security/ir.model.access.csv',
        'views/repair_menus.xml',
        'views/repair_views.xml',
        'report/repair_checklist_report.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': True,
    'license': 'LGPL-3',
}
