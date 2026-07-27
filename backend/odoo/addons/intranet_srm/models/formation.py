from odoo import models, fields


class Formation(models.Model):
    _name = 'intranet.formation'
    _description = 'Formation Intranet'
    _rec_name = 'nom'

    nom = fields.Char('Nom', required=True)
    description = fields.Text('Description')
    formateur = fields.Char('Formateur')
    date_debut = fields.Datetime('Date de début')
    date_fin = fields.Datetime('Date de fin')
    lieu = fields.Char('Lieu')
    category = fields.Selection([
        ('technique', 'Technique'),
        ('management', 'Management'),
        ('securite', 'Sécurité'),
        ('qualite', 'Qualité'),
        ('autre', 'Autre'),
    ], string='Catégorie', default='autre')
    max_participants = fields.Integer('Nombre max de participants')
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('published', 'Publiée'),
        ('closed', 'Clôturée'),
    ], string='État', default='draft')
    active = fields.Boolean('Actif', default=True)
    image = fields.Image('Image', max_width=1920, max_height=1920)
    created_at = fields.Datetime('Date de création', default=fields.Datetime.now, readonly=True)
