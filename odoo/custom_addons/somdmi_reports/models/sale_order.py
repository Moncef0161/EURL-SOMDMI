# -*- coding: utf-8 -*-
from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    invoice_type = fields.Selection([
        ('service', 'Service'),
        ('vente', 'Vente'),
        ('export_a', 'Exportation de service Type A'),
        ('export_b', 'Exportation de service Type B'),
    ], string='Type de Facturation',
       help='Sélectionnez le type de facturation pour utiliser le journal approprié')

    def _prepare_invoice(self):
        invoice_vals = super(SaleOrder, self)._prepare_invoice()
        if self.invoice_type:
            invoice_vals['invoice_type'] = self.invoice_type
            
            # Map invoice types to journal XML IDs
            journal_map = {
                'service': 'somdmi_reports.journal_service',
                'vente': 'somdmi_reports.journal_vente',
                'export_a': 'somdmi_reports.journal_export_a',
                'export_b': 'somdmi_reports.journal_export_b',
            }
            
            journal_xmlid = journal_map.get(self.invoice_type)
            if journal_xmlid:
                try:
                    journal = self.env.ref(journal_xmlid)
                    if journal:
                        invoice_vals['journal_id'] = journal.id
                except ValueError:
                    pass
                    
        return invoice_vals
