from odoo import models, fields, api

class CustomMaintenanceRequest(models.Model):
    _inherit = 'maintenance.request'
    x_new_field = fields.Char('New Field')
    owner_partner_id = fields.Many2one('res.partner', string='Owner')

class CustomMaintenanceEquipment(models.Model):
    _inherit = 'maintenance.equipment'
    owner_partner_id = fields.Many2one('res.partner', string='Owner')