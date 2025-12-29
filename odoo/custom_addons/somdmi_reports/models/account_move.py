# -*- coding: utf-8 -*-
from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    invoice_type = fields.Selection([
        ('service', 'Service'),
        ('vente', 'Vente'),
        ('export_a', 'Exportation de service Type A'),
        ('export_b', 'Exportation de service Type B'),
    ], string='Type de Facturation', 
       help='Sélectionnez le type de facturation pour utiliser le journal approprié')

    @api.onchange('invoice_type')
    def _onchange_invoice_type(self):
        """Update journal based on selected invoice type"""
        if self.invoice_type and self.move_type in ('out_invoice', 'out_refund'):
            journal_map = {
                'service': 'somdmi_reports.journal_service',
                'vente': 'somdmi_reports.journal_vente',
                'export_a': 'somdmi_reports.journal_export_a',
                'export_b': 'somdmi_reports.journal_export_b',
            }
            
            journal_xmlid = journal_map.get(self.invoice_type)
            if journal_xmlid:
                journal = self.env.ref(journal_xmlid, raise_if_not_found=False)
                if journal:
                    self.journal_id = journal.id

    @api.model_create_multi
    def create(self, vals_list):
        """Override create to set journal based on invoice type"""
        for vals in vals_list:
            if vals.get('invoice_type') and vals.get('move_type') in ('out_invoice', 'out_refund'):
                journal_map = {
                    'service': 'somdmi_reports.journal_service',
                    'vente': 'somdmi_reports.journal_vente',
                    'export_a': 'somdmi_reports.journal_export_a',
                    'export_b': 'somdmi_reports.journal_export_b',
                }
                
                journal_xmlid = journal_map.get(vals['invoice_type'])
                if journal_xmlid:
                    journal = self.env.ref(journal_xmlid, raise_if_not_found=False)
                    if journal and not vals.get('journal_id'):
                        vals['journal_id'] = journal.id
        
        return super(AccountMove, self).create(vals_list)

    def action_post(self):
        """Override action_post to set sequence if journal has one"""
        for move in self:
            if move.name == '/' and move.journal_id.sequence_id:
                move.name = move.journal_id.sequence_id.next_by_id()
        return super(AccountMove, self).action_post()
