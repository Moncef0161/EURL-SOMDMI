from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date
import requests

class CurrencyRateUpdater(models.Model):
    _inherit = 'res.currency'

    rate_with_margin = fields.Float(
        string="Rate with Margin",
        compute="_compute_rate_with_margin",
    )

    @api.depends("rate")
    def _compute_rate_with_margin(self):
        margin = float(self.env["ir.config_parameter"].sudo().get_param("algerian_accounting.invoice_error_margin", 0.0))
        for currency in self:
            currency.rate_with_margin = currency.rate + margin

    @api.model
    def update_currency_rates(self):
        auto_update = access_key = self.env['ir.config_parameter'].sudo().get_param('auto_update_currency_rates')
        if not auto_update:
            return
        url = self.env['ir.config_parameter'].sudo().get_param('currency_api_url')
        access_key = self.env['ir.config_parameter'].sudo().get_param('currency_api_key')
        if not access_key:
            raise ValidationError("Currency API Key is not set.")
        params = {
            "access_key": access_key
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            rates = data.get('rates', {})
            today = fields.Date.today()

            active_currencies = self.env['res.currency'].search([('active', '=', True)])
            company_currency = self.env.company.currency_id.name

            for currency in active_currencies:
                if currency.name == company_currency:
                    rate = 1.0
                else:
                    if company_currency == "EUR":  # return ta3 api daymen b euro donc on traite had le cas separement
                        rate = rates.get(currency.name)
                    else:
                        eur_to_target = rates.get(currency.name)
                        eur_to_company = rates.get(company_currency)
                        if eur_to_target and eur_to_company:
                            rate = eur_to_target / eur_to_company
                        else:
                            rate = None

                if rate:
                    rate_model = self.env['res.currency.rate']
                    existing_rate = rate_model.search([
                        ('currency_id', '=', currency.id),
                        ('company_id', '=', self.env.company.id),
                        ('name', '=', today)
                    ], limit=1)

                    if existing_rate:
                        existing_rate.rate = rate
                    else:
                        rate_model.sudo().create({
                            'currency_id': currency.id,
                            'rate': rate,
                            'name': today,
                            'company_id': self.env.company.id
                        })


