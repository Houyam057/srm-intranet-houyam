import json
from odoo import models, fields, api


class ChatbotConversation(models.Model):
    _name = 'chatbot.conversation'
    _description = 'Conversation Chatbot'
    _rec_name = 'name'
    _order = 'updated_at DESC'

    name = fields.Char('Titre', compute='_compute_name', store=True)
    user_id = fields.Many2one('res.users', string='Utilisateur', required=True, ondelete='cascade')
    messages = fields.Text('Messages', default='[]')
    message_count = fields.Integer('Nombre de messages', compute='_compute_message_count')
    created_at = fields.Datetime('Créé le', default=fields.Datetime.now, readonly=True)
    updated_at = fields.Datetime('Mis à jour le', default=fields.Datetime.now)

    @api.depends('messages')
    def _compute_message_count(self):
        for rec in self:
            try:
                msgs = json.loads(rec.messages or '[]')
                rec.message_count = len(msgs)
            except (json.JSONDecodeError, TypeError):
                rec.message_count = 0

    @api.depends('messages')
    def _compute_name(self):
        for rec in self:
            try:
                msgs = json.loads(rec.messages or '[]')
                first_user_msg = next((m['content'] for m in msgs if m.get('role') == 'user'), 'Nouvelle conversation')
                rec.name = first_user_msg[:50] + ('...' if len(first_user_msg) > 50 else '')
            except (json.JSONDecodeError, TypeError, KeyError, StopIteration):
                rec.name = 'Nouvelle conversation'

    def add_message(self, role, content):
        self.ensure_one()
        try:
            msgs = json.loads(self.messages or '[]')
        except (json.JSONDecodeError, TypeError):
            msgs = []
        msgs.append({'role': role, 'content': content})
        self.write({
            'messages': json.dumps(msgs),
            'updated_at': fields.Datetime.now(),
        })

    def get_messages(self):
        self.ensure_one()
        try:
            return json.loads(self.messages or '[]')
        except (json.JSONDecodeError, TypeError):
            return []
