from odoo import models, fields


class Pole(models.Model):
    _name = 'intranet.pole'
    _description = 'Pôle'
    _rec_name = 'name'

    name = fields.Char('Nom du Pôle', required=True)
    description = fields.Text('Description')

    def __str__(self):
        return self.name


class PoleOld(models.Model):
    _name = 'intranet.pole_old'
    _description = 'Pôle de Direction (ancien)'
    _rec_name = 'name'

    name = fields.Char('Nom du Pôle', required=True)
    description = fields.Text('Description')

    def __str__(self):
        return self.name
