from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date
import requests

class CurrencyRateUpdater(models.Model):
    _inherit = 'res.currency'

    @api.model
    def update_currency_rates(self):
        url = "https://api.exchangeratesapi.io/v1/latest"
        access_key = self.env['ir.config_parameter'].sudo().get_param('currency_api_key')
        if not access_key:
            raise ValidationError("Currency API Key is not set.")
        params = {
            "access_key": access_key
        }
        response = requests.get(url, params=params)
        print(15)
        if response.status_code == 200:
            print(17)
            data = response.json()
            rates = data.get('rates', {})
            today = fields.Date.today()

            active_currencies = self.env['res.currency'].search([('active', '=', True)])
            company_currency = self.env.company.currency_id.name

            for currency in active_currencies:
                if currency.name == company_currency:
                    print(27)
                    rate = 1.0
                else:
                    if company_currency == "EUR":  # return ta3 api daymen b euro donc on traite had le cas separement
                        print(31)
                        rate = rates.get(currency.name)
                    else:
                        print(34)
                        eur_to_target = rates.get(currency.name)
                        eur_to_company = rates.get(company_currency)
                        if eur_to_target and eur_to_company:
                            rate = eur_to_target / eur_to_company
                        else:
                            print(40)
                            rate = None

                if rate:
                    print(44)
                    rate_model = self.env['res.currency.rate']
                    existing_rate = rate_model.search([
                        ('currency_id', '=', currency.id),
                        ('company_id', '=', self.env.company.id),
                        ('name', '=', today)
                    ], limit=1)

                    if existing_rate:
                        print(53)
                        existing_rate.rate = rate
                    else:
                        print(56)
                        rate_model.sudo().create({
                            'currency_id': currency.id,
                            'rate': rate,
                            'name': today,
                            'company_id': self.env.company.id
                        })
                        print(63)


