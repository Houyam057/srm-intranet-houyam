from odoo import models, fields

class DirectionOld(models.Model):
    _name = 'intranet.direction_old'
    _description = 'Direction (ancien)'
    _rec_name = 'name'

    name = fields.Char('Nom de la Direction', required=True)
    code = fields.Char('Code')
    description = fields.Text('Description')
    active = fields.Boolean('Actif', default=True)

    def __str__(self):
        return self.name
