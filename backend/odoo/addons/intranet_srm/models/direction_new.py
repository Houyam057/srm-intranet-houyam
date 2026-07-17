from odoo import models, fields

class DirectionNew(models.Model):
    _name = 'intranet.direction'
    _description = 'Direction'
    _rec_name = 'name'

    name = fields.Char('Nom', required=True)
    description = fields.Text('Description')
    manager_id = fields.Many2one('intranet.user', string='Manager')
    manager_name = fields.Char('Nom du Manager', related='manager_id.name', store=True)

    direction_p_id = fields.Many2one('intranet.direction_p', string='Direction Principale')
    direction_p_name = fields.Char('Direction P', related='direction_p_id.name', store=True)

    sub_direction_ids = fields.One2many('intranet.sub_direction', 'direction_id', string='Sous-Directions')
    sub_direction_count = fields.Integer('Nombre de Sous-Directions', compute='_compute_sub_direction_count', store=True)

    active = fields.Boolean('Actif', default=True)
    created_at = fields.Datetime('Date de création', default=fields.Datetime.now)

    def _compute_sub_direction_count(self):
        for record in self:
            record.sub_direction_count = len(record.sub_direction_ids)

    def __str__(self):
        return self.name
