from odoo import models, fields, api

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    is_atelier_in = fields.Boolean(
        string="Is Atelier Reception",
        compute='_compute_is_atelier_in',
        store=False
    )

    @api.depends('picking_type_id', 'picking_type_id.sequence_code')
    def _compute_is_atelier_in(self):
        for picking in self:
            picking.is_atelier_in = picking.picking_type_id.sequence_code == 'ATEL-IN'

    def action_generate_repairs(self):
        self.ensure_one()
        repair_model = self.env['repair.order']
        new_repair_ids = []

        for move in self.move_ids_without_package:
            qty = int(move.product_uom_qty)
            for _ in range(qty):
                repair = repair_model.create({
                    'product_id': move.product_id.id,
                    'lot_id': move.x_lot_id.id,
                    'partner_id': self.partner_id.id,
                    'product_uom': move.product_uom.id,
                    'picking_id': self.id,
                    'declared_breakdown_ids': [(6, 0, move.x_declared_breakdown_ids.ids)],
                    'x_observation': move.x_observation,
                    'internal_notes': move.x_observation,
                })
                new_repair_ids.append(repair.id)

        # This is the part that redirects you
        return {
            'name': 'Ordres de Réparation Générés',
            'type': 'ir.actions.act_window',
            'res_model': 'repair.order',
            'view_mode': 'list,form',
            'domain': [('id', 'in', new_repair_ids)],  # Only show the ones we just made
            'target': 'current',  # Opens in the same window
        }

    def button_validate(self):
        # 1. Look through each line in the 'Operations' tab
        for move in self.move_ids_without_package:
            # 2. If the user filled in our custom Serial Number field
            if move.x_lot_id:
                # 3. If Odoo hasn't created the internal move lines yet, create one
                if not move.move_line_ids:
                    self.env['stock.move.line'].create({
                        'picking_id': self.id,
                        'move_id': move.id,
                        'product_id': move.product_id.id,
                        'product_uom_id': move.product_uom.id,
                        'location_id': move.location_id.id,
                        'location_dest_id': move.location_dest_id.id,
                        'lot_id': move.x_lot_id.id,
                        'quantity': move.product_uom_qty,
                    })
                else:
                    # 4. If lines exist (like after 'Mark as Todo'), sync the serial number
                    for line in move.move_line_ids:
                        if not line.lot_id:
                            line.write({
                                'lot_id': move.x_lot_id.id,
                                'quantity': move.product_uom_qty or 1.0
                            })

        # 5. Now continue with Odoo's standard validation logic
        return super(StockPicking, self).button_validate()

    @api.model
    def default_get(self, fields_list):
        res = super(StockPicking, self).default_get(fields_list)

        # Check if we are coming from reception menu
        if self._context.get('picking_ateliers_flow'):
            atelier_type = self.env.ref('atelier_repair.picking_type_atelier_in', raise_if_not_found=False)
            if atelier_type:
                res.update({
                    'picking_type_id': atelier_type.id,
                    'location_id': atelier_type.default_location_src_id.id,
                    'location_dest_id': atelier_type.default_location_dest_id.id,
                })
        
        # Check if we are coming from delivery menu
        elif self._context.get('picking_ateliers_delivery_flow'):
            atelier_type = self.env.ref('atelier_repair.picking_type_atelier_out', raise_if_not_found=False)
            if atelier_type:
                res.update({
                    'picking_type_id': atelier_type.id,
                    'location_id': atelier_type.default_location_src_id.id,
                    'location_dest_id': atelier_type.default_location_dest_id.id,
                })
        
        return res