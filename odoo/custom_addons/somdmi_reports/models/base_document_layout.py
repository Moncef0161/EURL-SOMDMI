from odoo import models, fields

class BaseDocumentLayout(models.TransientModel):
    _inherit = 'base.document.layout'

    company_registry = fields.Char(related='company_id.company_registry', readonly=True)
    nif = fields.Char(related='company_id.nif', readonly=True)
    nis = fields.Char(related='company_id.nis', readonly=True)
    nart = fields.Char(related='company_id.nart', readonly=True)
    nrc = fields.Char(related='company_id.nrc', readonly=True)
    rib = fields.Char(related='company_id.rib', readonly=True)
    state_id = fields.Many2one(related='company_id.state_id', readonly=True)
