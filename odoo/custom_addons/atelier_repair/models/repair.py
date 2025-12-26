# -*- coding: utf-8 -*-
from odoo import models, fields, api

# Electrofusion Checklist Data
ELECTROFUSION_ITEMS = [
    ('Nettoyage', 'Boitier/Châssis/Faisceaux'),
    ('Contrôles visuels aspect extérieur', 'Boitier'),
    ('Contrôles visuels aspect extérieur', 'Châssis'),
    ('Contrôles visuels aspect extérieur', 'Fixation boitier/châssis'),
    ('Contrôles visuels aspect extérieur', 'Lexan'),
    ('Contrôles visuels aspect extérieur', 'Afficheur LCD'),
    ('Contrôles visuels aspect extérieur', 'Faisceau primaire'),
    ('Contrôles visuels aspect extérieur', 'Prise secteur conforme au poste'),
    ('Contrôles visuels aspect extérieur', 'Adapt. prise CE/Domestique conforme'),
    ('Contrôles visuels aspect extérieur', 'Faisceau secondaire + Connectique'),
    ('Contrôles visuels aspect extérieur', 'Presse-étoupes'),
    ('Contrôles visuels aspect extérieur', 'Connecteurs secondaire'),
    ('Contrôles visuels aspect extérieur', 'Crayon lecteur'),
    ('Contrôles visuels aspect extérieur', 'Cordon crayon lect + Connectique'),
    ('Contrôles visuels aspect extérieur', 'Interrupteur M/A'),
    ('Contrôles visuels aspect extérieur', 'Sonde de température'),
    ('Contrôles visuels aspect extérieur', 'Ports externes'),
    ('Contrôles visuels aspect extérieur', 'Etiquette signalétique'),
    ('Contrôles visuels aspect extérieur', 'Présence scellé inviolable'),
    ('Contrôles visuels aspect extérieur', 'Sacoche/Coffre aluminium'),
    ('Contrôles sous tension', 'Edition historique'),
    ('Contrôles sous tension', 'Effacement de l\'historique'),
    ('Contrôles sous tension', 'Fonctionnement du buzzer'),
    ('Contrôles sous tension', 'Mode test conforme'),
    ('Contrôles sous tension', 'Essais de fonctionnement'),
    ('Contrôles visuels et opérations internes', 'Câblage'),
    ('Contrôles visuels et opérations internes', 'Fixation éléments'),
    ('Contrôles visuels et opérations internes', 'Platines électroniques'),
    ('Contrôles visuels et opérations internes', 'MàJ électronique'),
    ('Contrôles visuels et opérations internes', 'MàJ logiciel'),
    ('Contrôles visuels et opérations internes', 'Essais de fonctionnement'),
    ('Contrôles visuels et opérations internes', 'Fermeture poste'),
    ('Contrôles visuels et opérations internes', 'Pose du scellé inviolable'),
    ('Contrôle final', 'Paramétrage'),
    ('Contrôle final', 'Relevé d\'essais finals'),
    ('Contrôle final', 'Pose macaron de prochain contrôle')
]

# Bout à Bout Checklist Data
BOUT_A_BOUT_ITEMS = [
    ('Etapes Chronologiques', 'Test de déplacement'),
    ('Etapes Chronologiques', 'Test de pression'),
    ('Etapes Chronologiques', 'Vérification d\'élément chauffant'),
    ('Etapes Chronologiques', 'Vérification rabot'),
    ('Etapes Chronologiques', 'Vérification bâti'),
    ('Contrôles du Bâti', 'Connexions hydrauliques'),
    ('Contrôles du Bâti', 'Etat et fonctionnement libre des écrous de mors'),
    ('Contrôles du Bâti', 'Etat des surfaces bâti – mors – vérins'),
    ('Contrôles du Bâti', 'Plaque signalétique correctement renseignée'),
    ('Contrôles du Rabot', 'Etat général'),
    ('Contrôles du Rabot', 'Etat des Lames'),
    ('Contrôles du Rabot', 'Translation libre'),
    ('Contrôles de l\'Elément Chauffant', 'Etat Surface & revêtement Téflon'),
    ('Contrôles de l\'Elément Chauffant', 'Libre fonctionnement mécanique'),
    ('Contrôles de l\'Elément Chauffant', 'Etat carter de protection'),
    ('Contrôles de l\'Unité Hydraulique', 'Etat des boutons, leviers, mano'),
    ('Contrôles de l\'Unité Hydraulique', 'Fixation des sous ensembles'),
    ('Contrôles de l\'Unité Hydraulique', 'Etat des flexibles et connecteurs rapides'),
    ('Contrôles de l\'Unité Hydraulique', 'Vérification du niveau d\'huile'),
    ('Machine Automatique', 'Déroulement du cycle'),
    ('Machine Automatique', 'Aspect bourrelet'),
    ('Machine Automatique', 'Edition du ticket de cycle')
]

class RepairBreakdown(models.Model):
    _name = 'repair.breakdown'
    _description = 'Panne d\'Atelier'

    name = fields.Char(string='Nom de la Panne', required=True)

class RepairOrder(models.Model):
    _inherit = 'repair.order'

    brand_id = fields.Many2one(
        related='product_id.brand_id',
        readonly=False,
        store=False,
        string="Marque"
    )

    type_id = fields.Many2one(
        related='product_id.type_id',
        readonly=False,
        store=False,
        string="Type"
    )

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
    machine_type = fields.Selection([
        ('electrofusion', 'Electrofusion'),
        ('bout_a_bout', 'Bout à Bout')
    ], string='Type de Machine')
    checklist_ids = fields.One2many('repair.checklist.line', 'repair_id', string='Fiche de Contrôle')
    
    check_all_conforme = fields.Boolean(string='Tout Conforme')
    check_all_nc = fields.Boolean(string='Tout N.C')
    check_all_corrige = fields.Boolean(string='Tout Corrigé')

    # --- Bout à Bout Specific Fields (Hardcoded Layout) ---
    bb_serie_no = fields.Char(string='Série N°')
    bb_decharge_no = fields.Char(string='N° de décharge')
    
    # Diagnostique de la machine
    bb_diag_alimentation = fields.Boolean(string='Alimentation')
    bb_diag_pression = fields.Boolean(string='Pression')
    bb_diag_deplacement = fields.Boolean(string='Déplacement')
    bb_diag_temperature = fields.Boolean(string='Température')
    bb_diag_clavier = fields.Boolean(string='Clavier')
    bb_diag_autre = fields.Boolean(string='Autre')
    
    # ETAPES CHRONOLOGIQUES
    bb_chrono_deplacement = fields.Selection([('conforme', 'CONFIRME'), ('nc', 'N.C'), ('corrige', 'CORRIGE')], string='Test de déplacement')
    bb_chrono_pression = fields.Selection([('conforme', 'CONFIRME'), ('nc', 'N.C'), ('corrige', 'CORRIGE')], string='Test de pression')
    bb_chrono_element_chauffant = fields.Selection([('conforme', 'CONFIRME'), ('nc', 'N.C'), ('corrige', 'CORRIGE')], string='Vérification d\'élément chauffant')
    bb_chrono_rabot = fields.Selection([('conforme', 'CONFIRME'), ('nc', 'N.C'), ('corrige', 'CORRIGE')], string='Vérification rabot')
    bb_chrono_bati = fields.Selection([('conforme', 'CONFIRME'), ('nc', 'N.C'), ('corrige', 'CORRIGE')], string='Vérification bâti')
    
    # Footer 1
    bb_cycle_soudage = fields.Char(string='Cycle de soudage')
    bb_diam = fields.Char(string='DIAM')
    bb_conforme = fields.Boolean(string='Conforme')
    bb_impression_donnees = fields.Boolean(string='Impressionnes données')
    bb_date_reparation = fields.Date(string='Date de réparation', default=fields.Date.context_today)
    bb_remarque = fields.Text(string='Remarque')
    
    # Contrôles du Bâti
    bb_bati_connexions = fields.Boolean(string='Connexions hydrauliques')
    bb_bati_ecrous = fields.Boolean(string='Etat et fonctionnement libre des écrous de mors')
    bb_bati_surfaces = fields.Boolean(string='Etat des surfaces bâti – mors – vérins')
    bb_bati_plaque = fields.Boolean(string='Plaque signalétique correctement renseignée')
    
    # Contrôles du Rabot
    bb_rabot_etat = fields.Boolean(string='Etat général')
    bb_rabot_lames = fields.Boolean(string='Etat des Lames')
    bb_rabot_translation = fields.Boolean(string='Translation libre')
    
    # Contrôles de l'Elément Chauffant
    bb_chauffant_surface = fields.Boolean(string='Etat Surface & revêtement Téflon')
    bb_chauffant_mecanique = fields.Boolean(string='Libre fonctionnement mécanique')
    bb_chauffant_carter = fields.Boolean(string='Etat carter de protection')
    
    # Contrôles de l'Unité Hydraulique
    bb_hydraulique_boutons = fields.Boolean(string='Etat des boutons, leviers, mano. (Si manuelle)')
    bb_hydraulique_fixation = fields.Boolean(string='Fixation des sous ensembles')
    bb_hydraulique_flexibles = fields.Boolean(string='Etat des flexibles et connecteurs rapides')
    bb_hydraulique_huile = fields.Boolean(string='Vérification du niveau d\'huile')
    
    # Contrôles du Moniteur Informatisé
    bb_moniteur_etat = fields.Boolean(string='Etat général et fixations')
    
    # Contrôles de l'Unité Hydraulique (machine manuelle)
    bb_manuelle_levier = fields.Boolean(string='Fonctionnement levier Ouverture / Fermeture')
    bb_manuelle_regulateur = fields.Boolean(string='Fonctionnement régulateur pression')
    bb_manuelle_bypass = fields.Boolean(string='Fonctionnement du "By Pass"')
    
    # Pressure Table
    bb_pres_5 = fields.Float(string='5 Bar Actual')
    bb_pres_10 = fields.Float(string='10 Bar Actual')
    bb_pres_15 = fields.Float(string='15 Bar Actual')
    bb_pres_30 = fields.Float(string='30 Bar Actual')
    bb_pres_50 = fields.Float(string='50 Bar Actual')
    bb_pres_75 = fields.Float(string='75 Bar Actual')
    bb_pres_100 = fields.Float(string='100 Bar Actual')
    
    # Machine Automatique
    bb_auto_cycle = fields.Boolean(string='DEROULEMENT DU CYCLE')
    bb_auto_bourrelet = fields.Boolean(string='ASPECT BOURRELET')
    bb_auto_ticket = fields.Boolean(string='EDITION DU TICKET DE CYCLE')
    
    bb_observations = fields.Text(string='Observations / Evolutions')

    # --- Electrofusion Specific Fields (Hardcoded Layout) ---
    ef_serie_no = fields.Char(string='N° de Série')
    ef_op_no = fields.Char(string='N° OP')
    ef_mesure_appareil = fields.Selection([
        ('aoip', 'AOIP'),
        ('fluke', 'FLUKE 123'),
        ('autre', 'Autre')
    ], string='Type appareil de mesures')
    ef_mesure_serie = fields.Char(string='N° de série (Appareil)')
    ef_banc_serie = fields.Char(string='N° de série banc de test 10 gammes')
    
    # ETAPES CHRONOLOGIQUES (36 rows)
    # Using a simple naming convention for the 36 rows to keep it manageable
    ef_row1 = fields.Selection([('conforme', 'CONFORME'), ('nc', 'N.C.'), ('corrige', 'CORRIGE')], string='1. Nettoyage')
    ef_row2 = fields.Selection([('conforme', 'CONFORME'), ('nc', 'N.C.'), ('corrige', 'CORRIGE')], string='2. Boitier')
    ef_row3 = fields.Selection([('conforme', 'CONFORME'), ('nc', 'N.C.'), ('corrige', 'CORRIGE')], string='3. Châssis')
    ef_row4 = fields.Selection([('conforme', 'CONFORME'), ('nc', 'N.C.'), ('corrige', 'CORRIGE')], string='4. Fixation boitier/châssis')
    ef_row5 = fields.Selection([('conforme', 'CONFORME'), ('nc', 'N.C.'), ('corrige', 'CORRIGE')], string='5. Lexan')
    ef_row6 = fields.Selection([('conforme', 'CONFORME'), ('nc', 'N.C.'), ('corrige', 'CORRIGE')], string='6. Afficheur LCD')
    ef_row7 = fields.Selection([('conforme', 'CONFORME'), ('nc', 'N.C.'), ('corrige', 'CORRIGE')], string='7. Faisceau primaire')
    ef_row8 = fields.Selection([('conforme', 'CONFORME'), ('nc', 'N.C.'), ('corrige', 'CORRIGE')], string='8. Prise secteur conforme au poste')
    ef_row9 = fields.Selection([('conforme', 'CONFORME'), ('nc', 'N.C.'), ('corrige', 'CORRIGE')], string='9. Adapt. prise CE/Domestique conforme')
    ef_row10 = fields.Selection([('conforme', 'CONFORME'), ('nc', 'N.C.'), ('corrige', 'CORRIGE')], string='10. Faisceau secondaire + Connectique')
    ef_row11 = fields.Selection([('conforme', 'CONFORME'), ('nc', 'N.C.'), ('corrige', 'CORRIGE')], string='11. Presse-étoupes')
    ef_row12 = fields.Selection([('conforme', 'CONFORME'), ('nc', 'N.C.'), ('corrige', 'CORRIGE')], string='12. Connecteurs secondaire')
    ef_row13 = fields.Selection([('conforme', 'CONFORME'), ('nc', 'N.C.'), ('corrige', 'CORRIGE')], string='13. Crayon lecteur')
    ef_row14 = fields.Selection([('conforme', 'CONFORME'), ('nc', 'N.C.'), ('corrige', 'CORRIGE')], string='14. Cordon crayon lect + Connectique')
    ef_row15 = fields.Selection([('conforme', 'CONFORME'), ('nc', 'N.C.'), ('corrige', 'CORRIGE')], string='15. Interrupteur M/A')
    ef_row16 = fields.Selection([('conforme', 'CONFORME'), ('nc', 'N.C.'), ('corrige', 'CORRIGE')], string='16. Sonde de température')
    ef_row17 = fields.Selection([('conforme', 'CONFORME'), ('nc', 'N.C.'), ('corrige', 'CORRIGE')], string='17. Ports externes')
    ef_row18 = fields.Selection([('conforme', 'CONFORME'), ('nc', 'N.C.'), ('corrige', 'CORRIGE')], string='18. Etiquette signalétique')
    ef_row19 = fields.Selection([('conforme', 'CONFORME'), ('nc', 'N.C.'), ('corrige', 'CORRIGE')], string='19. Présence scellé inviolable')
    ef_row20 = fields.Selection([('conforme', 'CONFORME'), ('nc', 'N.C.'), ('corrige', 'CORRIGE')], string='20. Sacoche/Coffre aluminium')
    ef_row21 = fields.Selection([('conforme', 'CONFORME'), ('nc', 'N.C.'), ('corrige', 'CORRIGE')], string='21. Edition historique')
    ef_row22 = fields.Selection([('conforme', 'CONFORME'), ('nc', 'N.C.'), ('corrige', 'CORRIGE')], string='22. Effacement de l\'historique')
    ef_row23 = fields.Selection([('conforme', 'CONFORME'), ('nc', 'N.C.'), ('corrige', 'CORRIGE')], string='23. Fonctionnement du buzzer')
    ef_row24 = fields.Selection([('conforme', 'CONFORME'), ('nc', 'N.C.'), ('corrige', 'CORRIGE')], string='24. Mode test conforme')
    ef_row25 = fields.Selection([('conforme', 'CONFORME'), ('nc', 'N.C.'), ('corrige', 'CORRIGE')], string='25. Essais de fonctionnement')
    ef_row26 = fields.Selection([('conforme', 'CONFORME'), ('nc', 'N.C.'), ('corrige', 'CORRIGE')], string='26. Câblage')
    ef_row27 = fields.Selection([('conforme', 'CONFORME'), ('nc', 'N.C.'), ('corrige', 'CORRIGE')], string='27. Fixation éléments')
    ef_row28 = fields.Selection([('conforme', 'CONFORME'), ('nc', 'N.C.'), ('corrige', 'CORRIGE')], string='28. Platines électroniques')
    ef_row29 = fields.Selection([('conforme', 'CONFORME'), ('nc', 'N.C.'), ('corrige', 'CORRIGE')], string='29. MàJ électronique')
    ef_row30 = fields.Selection([('conforme', 'CONFORME'), ('nc', 'N.C.'), ('corrige', 'CORRIGE')], string='30. MàJ logiciel')
    ef_row31 = fields.Selection([('conforme', 'CONFORME'), ('nc', 'N.C.'), ('corrige', 'CORRIGE')], string='31. Essais de fonctionnement')
    ef_row32 = fields.Selection([('conforme', 'CONFORME'), ('nc', 'N.C.'), ('corrige', 'CORRIGE')], string='32. Fermeture poste')
    ef_row33 = fields.Selection([('conforme', 'CONFORME'), ('nc', 'N.C.'), ('corrige', 'CORRIGE')], string='33. Pose du scellé inviolable')
    ef_row34 = fields.Selection([('conforme', 'CONFORME'), ('nc', 'N.C.'), ('corrige', 'CORRIGE')], string='34. Paramétrage')
    ef_row35 = fields.Selection([('conforme', 'CONFORME'), ('nc', 'N.C.'), ('corrige', 'CORRIGE')], string='35. Relevé d\'essais finals')
    ef_row36 = fields.Selection([('conforme', 'CONFORME'), ('nc', 'N.C.'), ('corrige', 'CORRIGE')], string='36. Pose macaron de prochain contrôle')
    
    # Remplacements de Matériel
    ef_carte_usb = fields.Char(string='Carte USB Type – N°')
    ef_version_logiciel = fields.Char(string='Version logiciel')
    
    # RELEVE D’ESSAIS FINALS
    ef_test_1 = fields.Char(string='14 V / 0,25 Ω')
    ef_test_2 = fields.Char(string='24 V / 0,25 Ω')
    ef_test_3 = fields.Char(string='30 V / 0,40 Ω')
    ef_test_4 = fields.Char(string='42 V / 0,65 Ω')
    ef_test_5 = fields.Char(string='35 V / 1,00 Ω')
    ef_test_6 = fields.Char(string='39 V / 2,00 Ω')
    ef_test_7 = fields.Char(string='24 V / 5,00 Ω')
    ef_test_8 = fields.Char(string='30 V / 5,00 Ω')
    ef_test_9 = fields.Char(string='39 V / 10,0 Ω')
    ef_test_10 = fields.Char(string='42 V / 15,0 Ω')
    ef_test_manuel = fields.Char(string='Mode Manuel Result')
    
    ef_essais_autres = fields.Text(string='Autres essais')
    ef_observations = fields.Text(string='Observations')

    # New fields for Reception and Delivery
    reception_no = fields.Char(string='N° Bon de Réception', copy=False, readonly=True)
    livraison_no = fields.Char(string='N° Bon de Livraison', copy=False, readonly=True)
    devis_approx = fields.Float(string='Devis approx.')
    mode_paiement = fields.Selection([
        ('espece', 'Espèce'),
        ('cheque', 'Chèque'),
        ('virement', 'Virement'),
        ('autre', 'Autre')
    ], string='Mode de paiement', default='espece')
    timbre = fields.Float(string='Timbre')
    etabli_par = fields.Many2one('res.users', string='Etabli par', default=lambda self: self.env.user)
    
    amount_untaxed = fields.Float(string='Total HT', compute='_compute_amounts', store=True)
    amount_tax = fields.Float(string='Total TVA', compute='_compute_amounts', store=True)
    amount_total = fields.Float(string='Total TTC', compute='_compute_amounts', store=True)
    amount_net_payer = fields.Float(string='NET A PAYER', compute='_compute_amounts', store=True)

    @api.depends('move_ids.price_unit', 'move_ids.tax_id', 'move_ids.product_uom_qty', 'timbre')
    def _compute_amounts(self):
        for order in self:
            untaxed = 0.0
            tax = 0.0
            for move in order.move_ids:
                price = move.price_unit * move.product_uom_qty
                untaxed += price
                if move.tax_id:
                    taxes = move.tax_id.compute_all(move.price_unit, order.company_id.currency_id, move.product_uom_qty, product=move.product_id, partner=order.partner_id)
                    tax += sum(t.get('amount', 0.0) for t in taxes.get('taxes', []))
            order.amount_untaxed = untaxed
            order.amount_tax = tax
            order.amount_total = untaxed + tax
            order.amount_net_payer = untaxed + tax + order.timbre

    def action_generate_reception_no(self):
        for order in self:
            if not order.reception_no:
                order.reception_no = self.env['ir.sequence'].next_by_code('repair.reception.seq')

    def action_generate_livraison_no(self):
        for order in self:
            if not order.livraison_no:
                order.livraison_no = self.env['ir.sequence'].next_by_code('repair.livraison.seq')

    @api.onchange('checklist_ids')
    def _onchange_checklist_ids(self):
        if not self.checklist_ids:
            return

        # Check if all lines match the state
        all_conforme = all(line.is_conforme for line in self.checklist_ids)
        all_nc = all(line.is_nc for line in self.checklist_ids)
        all_corrige = all(line.is_corrige for line in self.checklist_ids)

        # Update the "Tout" checkboxes without triggering their onchanges if possible
        # In Odoo, assigning to a field in an onchange triggers other onchanges.
        # But we only want to update the UI state.
        if self.check_all_conforme != all_conforme:
            self.check_all_conforme = all_conforme
        if self.check_all_nc != all_nc:
            self.check_all_nc = all_nc
        if self.check_all_corrige != all_corrige:
            self.check_all_corrige = all_corrige

    @api.onchange('check_all_conforme')
    def _onchange_check_all_conforme(self):
        if self.check_all_conforme:
            self.check_all_nc = False
            self.check_all_corrige = False
            for line in self.checklist_ids:
                line.is_conforme = True
                line.is_nc = False
                line.is_corrige = False
        elif all(line.is_conforme for line in self.checklist_ids):
            # Only uncheck all if they were all checked (manual uncheck of the "Tout" box)
            for line in self.checklist_ids:
                line.is_conforme = False

    @api.onchange('check_all_nc')
    def _onchange_check_all_nc(self):
        if self.check_all_nc:
            self.check_all_conforme = False
            self.check_all_corrige = False
            for line in self.checklist_ids:
                line.is_nc = True
                line.is_conforme = False
                line.is_corrige = False
        elif all(line.is_nc for line in self.checklist_ids):
            for line in self.checklist_ids:
                line.is_nc = False

    @api.onchange('check_all_corrige')
    def _onchange_check_all_corrige(self):
        if self.check_all_corrige:
            self.check_all_conforme = False
            self.check_all_nc = False
            for line in self.checklist_ids:
                line.is_corrige = True
                line.is_conforme = False
                line.is_nc = False
        elif all(line.is_corrige for line in self.checklist_ids):
            for line in self.checklist_ids:
                line.is_corrige = False

    @api.onchange('machine_type')
    def _onchange_machine_type(self):
        if not self.machine_type:
            return
        
        # Clear existing lines
        self.checklist_ids = [(5, 0, 0)]
        
        lines = []
        if self.machine_type == 'electrofusion':
            items = ELECTROFUSION_ITEMS
        else: # bout_a_bout
            items = BOUT_A_BOUT_ITEMS
        
        for name, section in items:
            lines.append((0, 0, {
                'name': name,
                'section': section,
            }))
        self.checklist_ids = lines

class RepairChecklistLine(models.Model):
    _name = 'repair.checklist.line'
    _description = 'Ligne de Fiche de Contrôle'

    repair_id = fields.Many2one('repair.order', string='Ordre de Réparation', ondelete='cascade')
    name = fields.Char(string='Opération', required=True)
    section = fields.Char(string='Section')
    is_conforme = fields.Boolean(string='Conforme')
    is_nc = fields.Boolean(string='N.C')
    is_corrige = fields.Boolean(string='Corrigé')
    observation = fields.Text(string='Observation')
    
    # Pressure fields for Bout à Bout
    pressure_min = fields.Float(string='Pression Min')
    pressure_max = fields.Float(string='Pression Max')
    pressure_actual = fields.Float(string='Pression Réelle')

    @api.onchange('is_conforme')
    def _onchange_is_conforme(self):
        if self.is_conforme:
            self.is_nc = False
            self.is_corrige = False

    @api.onchange('is_nc')
    def _onchange_is_nc(self):
        if self.is_nc:
            self.is_conforme = False
            self.is_corrige = False

    @api.onchange('is_corrige')
    def _onchange_is_corrige(self):
        if self.is_corrige:
            self.is_conforme = False
            self.is_nc = False

class StockMove(models.Model):
    _inherit = 'stock.move'

    tax_id = fields.Many2many('account.tax', string='Taxes')

    @api.onchange('product_id')
    def _onchange_product_id_set_defaults(self):
        if self.product_id:
            # Set price_unit to the product's list price
            self.price_unit = self.product_id.list_price
            # Set tax_id to the default tax (assuming it's the first tax in the company's default taxes)
            company = self.env.company
            default_tax = self.env['account.tax'].search([('company_id', '=', company.id), ('type_tax_use', '=', 'sale')], limit=1)
            if default_tax:
                self.tax_id = [(6, 0, [default_tax.id])]

class ProductBrand(models.Model):
    _name = 'product.brand'
    _description = 'Marque de Produit'

    name = fields.Char(string='Nom', required=True)

class ProductType(models.Model):
    _name = 'product.type'
    _description = 'Type de Machine'

    name = fields.Char(string='Nom', required=True)
    brand_id = fields.Many2one('product.brand', string='Marque', required=True)

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    brand_id = fields.Many2one('product.brand', string='Marque')
    type_id = fields.Many2one('product.type', string='Type')
    state = fields.Selection([
        ('new', 'Neuf'),
        ('used', 'Usagé'),
        ('refurbished', 'Remis à neuf'),
    ], string='État')

    def _formatted_name(self, base_name=None):
        self.ensure_one()
        name = base_name or self.name or ""
        if self.brand_id and self.type_id:
            name = f"{self.brand_id.name} {self.type_id.name} {name}"
        return name

    @api.model
    def create(self, vals):
        name = vals.get("name")
        brand = vals.get("brand_id")
        type_ = vals.get("type_id")

        if brand and type_ and name:
            brand_rec = self.env["product.brand"].browse(brand)
            type_rec = self.env["product.type"].browse(type_)
            vals["name"] = f"{brand_rec.name} {type_rec.name} {name}"

        return super(ProductTemplate, self).create(vals)

    def write(self, vals):
        res = super(ProductTemplate, self).write(vals)

        fields_trigger = ("name" in vals or
                          "brand_id" in vals or
                          "type_id" in vals)

        if fields_trigger:
            for rec in self:
                rec.name = rec._formatted_name()

        return res


