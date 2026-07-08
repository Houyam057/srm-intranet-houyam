from odoo import models, fields, api
from datetime import datetime, timedelta

class News(models.Model):
    _name = 'intranet.news'
    _description = 'Actualité'
    _rec_name = 'title'
    _order = 'published_date DESC'

    PRIORITY_SELECTION = [
        ('low', 'Basse'),
        ('medium', 'Moyenne'),
        ('high', 'Haute'),
        ('urgent', 'Urgent'),
    ]

    title = fields.Char('Titre', required=True)
    content = fields.Html('Contenu')
    summary = fields.Text('Résumé')
    
    image = fields.Binary('Image')
    image_url = fields.Char('URL Image')
    
    author_id = fields.Many2one('intranet.employee', string='Auteur')
    author_name = fields.Char('Nom de l\'auteur', related='author_id.name', store=True)
    
    priority = fields.Selection(PRIORITY_SELECTION, string='Priorité', default='medium')
    category = fields.Char('Catégorie', default='Actualité')
    
    published_date = fields.Datetime('Date de publication', default=fields.Datetime.now)
    published = fields.Boolean('Publiée', default=True)
    
    view_count = fields.Integer('Nombre de vues', default=0)
    created_at = fields.Datetime('Date de création', default=fields.Datetime.now)

    @api.model
    def get_recent_news(self, limit=5):
        """Retourne les actualités récentes"""
        return self.search([('published', '=', True)], order='published_date DESC', limit=limit)

    def __str__(self):
        return self.title
