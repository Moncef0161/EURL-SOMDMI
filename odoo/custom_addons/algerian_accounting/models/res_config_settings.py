from odoo import models, fields

class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    invoice_error_margin = fields.Float(
        string="Error Margin",
        config_parameter="algerian_accounting.invoice_error_margin",
    )