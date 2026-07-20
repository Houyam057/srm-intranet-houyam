from odoo import models, fields


class Formation(models.Model):
    _name = 'intranet.formation'
    _description = 'Formation Intranet'
    _rec_name = 'nom'
    _auto = True
    _table = 'intranet_formation'

    nom = fields.Char('Nom', readonly=True)
    date_ajout = fields.Datetime('Date ajout', readonly=True)
    date_fin = fields.Datetime('Date fin', readonly=True)
