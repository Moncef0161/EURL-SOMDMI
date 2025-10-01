from odoo import models, fields

class RepairOrder(models.Model):
    _inherit = "repair.order"

    product_id = fields.Many2one(
        'product.product',
        string="Product to Repair",
        domain="[('repair_ok', '=', True)]"
    )
