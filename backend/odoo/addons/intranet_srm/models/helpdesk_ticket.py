from odoo import models, fields

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

    employee_id = fields.Many2one('intranet.user', string='Demandeur')
    subject = fields.Char('Sujet', required=True)
    category = fields.Char('Catégorie')
    message = fields.Text('Message', required=True)
    status = fields.Selection(STATUS_SELECTION, string='Statut', default='new', required=True)

    created_at = fields.Datetime('Date de création', default=fields.Datetime.now)
