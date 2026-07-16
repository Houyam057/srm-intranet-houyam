from odoo import models, fields, api

class Feedback(models.Model):
    _name = 'intranet.feedback'
    _description = 'Feedback/Baromètre de satisfaction'
    _rec_name = 'id'

    MOOD_SELECTION = [
        ('very_bad', '😢 Très mauvais'),
        ('bad', '😞 Mauvais'),
        ('neutral', '😐 Neutre'),
        ('good', '😊 Bon'),
        ('very_good', '😄 Très bon'),
    ]

    employee_id = fields.Many2one('intranet.user', string='Utilisateur')
    mood = fields.Selection(MOOD_SELECTION, string='Sentiment', required=True)
    comment = fields.Text('Commentaire')
    
    category = fields.Char('Catégorie', default='Général')
    anonymous = fields.Boolean('Anonyme', default=False)
    
    created_at = fields.Datetime('Date de création', default=fields.Datetime.now)

    @api.model
    def get_mood_stats(self):
        """Retourne les statistiques de satisfaction"""
        stats = {}
        for mood in dict(self.MOOD_SELECTION):
            count = self.search_count([('mood', '=', mood)])
            stats[mood] = count
        return stats

    def __str__(self):
        return f"Feedback - {self.mood}"
