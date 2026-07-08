from odoo import models, fields

class Pole(models.Model):
    _name = 'intranet.pole'
    _description = 'Pôle de Direction'
    _rec_name = 'name'

    name = fields.Char('Nom du Pôle', required=True)
    description = fields.Text('Description')
    direction_ids = fields.One2many('intranet.direction', 'pole_id', string='Directions')

    def __str__(self):
        return self.name
