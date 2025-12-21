{
    "name": "Algerian Accounting",
    "author": "Riad Bensemmane",
    "version": "18.0.0.1.0",
    "depends": ["l10n_dz"],
    "data": [
        'views/algerian_accounting_views.xml',
        'views/res_config_settings_views.xml',
        'views/res_currency_views.xml',
        'data/ir_cron_currency_update.xml',
    ],
    'post_init_hook': 'populate_algeria_wilayas',
    "installable": True,
    "auto_install": True,
}