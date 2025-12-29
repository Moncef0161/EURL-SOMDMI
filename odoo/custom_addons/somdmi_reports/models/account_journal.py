# -*- coding: utf-8 -*-
from odoo import models, fields

class AccountJournal(models.Model):
    _inherit = 'account.journal'

    sequence_id = fields.Many2one('ir.sequence', string='Entry Sequence',
        help="This sequence will be used to generate the journal entry name.")
