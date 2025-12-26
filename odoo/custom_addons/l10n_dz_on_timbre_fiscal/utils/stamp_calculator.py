import math

class StampCalculator:
    def __init__(self, env):
        self.env = env

    def calculate(self, montant):
        res = {}
        montant_timbre = 0.0
        droit = 0.0

        # Utilisation de math.ceil pour arrondir à la tranche de 100 DA supérieure
        tranche_arrondie = math.ceil(montant / 100.0) * 100

        if montant <= 30_000:
            droit = tranche_arrondie * 0.01
        elif montant <= 100_000:
            droit = tranche_arrondie * 0.015
        else:
            droit = tranche_arrondie * 0.02

        # Minimum de 5 DA et arrondi au Dinar supérieur (math.ceil)
        if montant > 300:
            montant_timbre = max(math.ceil(droit), 5)

        res['timbre'] = montant_timbre
        res['amount_timbre'] = montant + montant_timbre

        return res

    def GetStampAccount(self, move_type):
        if move_type in ('out_invoice', 'out_refund'):
            return self.env['ir.config_parameter'].sudo().get_param('l10n_dz_on_timbre_fiscal.stamp_sale_account_id')
        if move_type in ('in_invoice', 'in_refund'):
            return self.env['ir.config_parameter'].sudo().get_param('l10n_dz_on_timbre_fiscal.stamp_purchase_account_id')

        return False