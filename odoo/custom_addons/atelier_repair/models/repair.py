# -*- coding: utf-8 -*-
from odoo import models, fields, api

class RepairBreakdown(models.Model):
    _name = 'repair.breakdown'
    _description = 'Panne d\'Atelier'

    name = fields.Char(string='Nom de la Panne', required=True)

class RepairOrder(models.Model):
    _inherit = 'repair.order'

    declared_breakdown_ids = fields.Many2many(
        'repair.breakdown', 
        'repair_order_declared_breakdown_rel',
        'repair_id', 
        'breakdown_id',
        string='Pannes déclarées', 
        required=True
    )
    actual_breakdown_ids = fields.Many2many(
        'repair.breakdown', 
        'repair_order_actual_breakdown_rel',
        'repair_id', 
        'breakdown_id',
        string='Pannes réelles', 
        required=True
    )
