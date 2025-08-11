from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re

class ResPartner(models.Model):
    _inherit = 'res.partner'

    nis = fields.Char(string="NIS")
    nif = fields.Char(string="NIF")
    rib = fields.Char(string="RIB")
    nrc = fields.Char(string="NRC")
    nart = fields.Char(string="NART")

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        if 'country_id' in fields and not res.get('country_id'):
            algeria = self.env.ref('base.dz', raise_if_not_found=False)
            if algeria:
                res['country_id'] = algeria.id
        return res

    def _check_exact_digits(self, value, length, label):
        if value and not re.fullmatch(r'\d{' + str(length) + '}', value):
            raise ValidationError(f"The {label} must be exactly {length} digits.")

    @api.constrains('nis', 'nif')
    def _check_nis_nif(self):
        for partner in self:
            partner._check_exact_digits(partner.nis, 15, "NIS")
            partner._check_exact_digits(partner.nif, 15, "NIF")
            partner._check_exact_digits(partner.rib, 20, "RIB")
