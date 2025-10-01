from odoo import fields, models

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    repair_ok = fields.Boolean(string="Repair")
