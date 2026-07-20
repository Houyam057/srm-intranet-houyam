from odoo import models, fields

class DirectionP(models.Model):
    _name = 'intranet.direction_p'
    _description = 'Direction Principale'
    _rec_name = 'name'

    name = fields.Char('Nom', required=True)
    code = fields.Char('Code')
    description = fields.Text('Description')
    manager_id = fields.Many2one('intranet.user', string='Manager')
    manager_name = fields.Char('Nom du Manager', related='manager_id.name', store=True)

    pole_id = fields.Many2one('intranet.pole', string='Pôle')
    pole_name = fields.Char('Nom du Pôle', related='pole_id.name', store=True)

    direction_ids = fields.One2many('intranet.direction', 'direction_p_id', string='Directions')
    direction_count = fields.Integer('Nombre de Directions', compute='_compute_direction_count', store=True)

    active = fields.Boolean('Actif', default=True)
    created_at = fields.Datetime('Date de création', default=fields.Datetime.now)

    def _compute_direction_count(self):
        for record in self:
            record.direction_count = len(record.direction_ids)

    def __str__(self):
        return self.name
