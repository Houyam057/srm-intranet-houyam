from odoo import models, fields


class Suggestion(models.Model):
    _name = 'intranet.suggestion'
    _description = 'Suggestion'
    _rec_name = 'title'

    title = fields.Char('Titre', required=True)
    category = fields.Selection([
        ('amelioration', 'Amélioration'),
        ('innovation', 'Innovation'),
        ('environnement', 'Environnement de travail'),
        ('processus', 'Processus'),
        ('autre', 'Autre'),
    ], string='Catégorie', default='amelioration')
    message = fields.Text('Message', required=True)
    author_id = fields.Many2one('res.users', string='Auteur', default=lambda self: self.env.user, readonly=True)
    author_name = fields.Char('Nom de l\'auteur', related='author_id.name', store=True)
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('submitted', 'Soumise'),
        ('reviewed', 'Examinée'),
        ('accepted', 'Acceptée'),
        ('rejected', 'Rejetée'),
    ], string='État', default='draft')
    active = fields.Boolean('Actif', default=True)
    created_at = fields.Datetime('Date de création', default=fields.Datetime.now, readonly=True)
