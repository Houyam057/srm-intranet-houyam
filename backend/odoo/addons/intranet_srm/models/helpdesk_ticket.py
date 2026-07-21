import logging
from pathlib import Path
from odoo import models, fields, api

_logger = logging.getLogger(__name__)

# ai_triage/ lives at the repo root, as a sibling of backend/, decoupled from this Odoo addon.
MODELS_DIR = Path(__file__).resolve().parents[5] / 'ai_triage' / 'models'
_urgency_model = None


def _load_urgency_model():
    global _urgency_model
    if _urgency_model is None:
        import joblib
        _urgency_model = joblib.load(MODELS_DIR / 'urgency_model.joblib')
    return _urgency_model


class HelpdeskTicket(models.Model):
    _name = 'intranet.helpdesk_ticket'
    _description = 'Ticket HelpDesk'
    _rec_name = 'subject'
    _order = 'created_at desc'

    STATUS_SELECTION = [
        ('new', 'Nouveau'),
        ('in_progress', 'En cours'),
        ('resolved', 'Résolu'),
    ]

    URGENCY_SELECTION = [
        ('low', 'Faible'),
        ('normal', 'Normale'),
        ('urgent', 'Urgente'),
    ]

    employee_id = fields.Many2one('intranet.user', string='Demandeur')
    subject = fields.Char('Sujet', required=True)
    category = fields.Char('Catégorie')
    message = fields.Text('Message', required=True)
    status = fields.Selection(STATUS_SELECTION, string='Statut', default='new', required=True)
    urgency = fields.Selection(URGENCY_SELECTION, string='Urgence')

    created_at = fields.Datetime('Date de création', default=fields.Datetime.now)

    def _predict_urgency(self, subject, message):
        try:
            model = _load_urgency_model()
            return model.predict([f"{subject or ''} {message or ''}"])[0]
        except Exception:
            _logger.exception("Echec de la prediction d'urgence, ticket cree sans urgence predite")
            return False

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('urgency'):
                vals['urgency'] = self._predict_urgency(vals.get('subject'), vals.get('message'))
        return super().create(vals_list)
