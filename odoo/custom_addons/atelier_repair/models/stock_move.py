from odoo import models, fields, api

class StockMove(models.Model):
    _inherit = 'stock.move'

    # Field for Serial Number with inline creation
    x_lot_id = fields.Many2one('stock.lot', string='Numéro de Série')
    x_observation = fields.Char(string='Observation')
    x_declared_breakdown_ids = fields.Many2many(
        'repair.breakdown',
        string='Pannes Déclarées'
    )

    def _prepare_merge_moves_distinct_fields(self):
        fields = super()._prepare_merge_moves_distinct_fields()
        fields.append('x_lot_id')
        fields.append('x_observation')
        return fields
