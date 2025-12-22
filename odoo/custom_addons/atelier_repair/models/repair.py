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
