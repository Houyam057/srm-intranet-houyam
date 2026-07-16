from odoo import models, fields, api


class HelpdeskTicket(models.Model):
    _name = 'intranet.helpdesk.ticket'
    _description = 'Ticket HelpDesk'
    _rec_name = 'subject'
    _order = 'created_at DESC'

    STATUS_SELECTION = [
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]

    subject = fields.Char('Sujet', required=True)
    category = fields.Char('Catégorie', required=True)
    message = fields.Text('Message', required=True)
    employee_id = fields.Many2one('intranet.user', string='Employé', default=lambda self: self._default_employee())
    status = fields.Selection(STATUS_SELECTION, string='Statut', default='new', required=True)
    created_at = fields.Datetime('Date de création', default=fields.Datetime.now)

    @api.model
    def _default_employee(self):
        employee = self.env['intranet.user'].sudo().browse(self.env.user.id)
        return employee.id if employee.exists() else False
