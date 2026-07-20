from odoo import models, fields


class Inscription(models.Model):
    _name = 'inscription.formation'
    _description = 'Inscription Formation'
    _auto = True
    _table = 'intranet_inscription_formation'
    _sql_constraints = [
        ('unique_inscription', 'UNIQUE(id_u, id_f)', 'Un utilisateur ne peut s\'inscrire qu\'une fois par formation.')
    ]

    ETAT_SELECTION = [
        ('en_attente', 'En attente'),
        ('inscrit', 'Inscrit'),
        ('termine', 'Terminé'),
    ]

    id_f = fields.Many2one('intranet.formation', string='Formation', readonly=True)
    id_u = fields.Many2one('intranet.user', string='Utilisateur', readonly=True)
    etat = fields.Selection(ETAT_SELECTION, string='État', readonly=True, default='en_attente')
    date_fin = fields.Datetime('Date fin', readonly=True)
