from odoo import models, fields

class SubDirection(models.Model):
    _name = 'intranet.sub_direction'
    _description = 'Sous-Direction'
    _rec_name = 'name'

    name = fields.Char('Nom', required=True)
    description = fields.Text('Description')
    manager_id = fields.Many2one('intranet.user', string='Manager')
    manager_name = fields.Char('Nom du Manager', related='manager_id.name', store=True)

    direction_id = fields.Many2one('intranet.direction', string='Direction')
    direction_name = fields.Char('Direction', related='direction_id.name', store=True)

    active = fields.Boolean('Actif', default=True)
    created_at = fields.Datetime('Date de création', default=fields.Datetime.now)

    def __str__(self):
        return self.name
