from odoo import models, fields

class DirectionNew(models.Model):
    _name = 'intranet.direction'
    _description = 'Direction'
    _rec_name = 'name'

    name = fields.Char('Nom', required=True)
    code = fields.Char('Code')
    description = fields.Text('Description')
    manager_id = fields.Many2one('intranet.user', string='Manager')
    manager_name = fields.Char('Nom du Manager', related='manager_id.name', store=True)

    pole_id = fields.Many2one('intranet.pole', string='Pôle')

    sub_direction_ids = fields.One2many('intranet.sub_direction', 'direction_id', string='Sous-Directions')
    sub_direction_count = fields.Integer('Nombre de Sous-Directions', compute='_compute_sub_direction_count', store=True)

    active = fields.Boolean('Actif', default=True)
    created_at = fields.Datetime('Date de création', default=fields.Datetime.now)

    def _compute_sub_direction_count(self):
        for record in self:
            record.sub_direction_count = len(record.sub_direction_ids)

    def __str__(self):
        return self.name
