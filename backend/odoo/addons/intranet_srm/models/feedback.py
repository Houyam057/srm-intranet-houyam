from odoo import models, fields, api
from datetime import timedelta


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

    @api.model
    def check_vote_cooldown(self):
        """Vérifie si l'utilisateur connecté peut voter. Retourne les infos de cooldown."""
        user = self.env.user
        now = fields.Datetime.now()
        employee = self.env['intranet.user'].search([('res_user_id', '=', user.id)], limit=1)
        if not employee:
            last_vote = self.search([
                ('employee_id', '=', False),
                ('anonymous', '=', True),
            ], order='created_at desc', limit=1)
            if not last_vote:
                return {'can_vote': True, 'next_vote_at': None, 'remaining_seconds': 0}
            cooldown_end = last_vote.created_at + timedelta(hours=24)
            remaining = int((cooldown_end - now).total_seconds())
            if remaining <= 0:
                return {'can_vote': True, 'next_vote_at': None, 'remaining_seconds': 0}
            return {'can_vote': False, 'next_vote_at': cooldown_end.isoformat(), 'remaining_seconds': remaining}

        last_vote = self.search([
            ('employee_id', '=', employee.id),
        ], order='created_at desc', limit=1)

        if not last_vote:
            return {'can_vote': True, 'next_vote_at': None, 'remaining_seconds': 0}

        cooldown_end = last_vote.created_at + timedelta(hours=24)
        remaining = int((cooldown_end - now).total_seconds())
        if remaining <= 0:
            return {'can_vote': True, 'next_vote_at': None, 'remaining_seconds': 0}
        return {'can_vote': False, 'next_vote_at': cooldown_end.isoformat(), 'remaining_seconds': remaining}

    def __str__(self):
        return f"Feedback - {self.mood}"
