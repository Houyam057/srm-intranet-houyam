from odoo import models, fields, api

class IntranetUser(models.Model):
    _name = 'intranet.user'
    _description = 'Utilisateur Intranet'
    _rec_name = 'name'

    name = fields.Char('Nom', required=True)
    prenom = fields.Char('Prénom', required=True)
    email = fields.Char('Email', required=True)
    phone = fields.Char('Numéro de téléphone')

    active = fields.Boolean('Actif', default=True)
    created_at = fields.Datetime('Date de création', default=fields.Datetime.now)

    _sql_constraints = [
        ('email_unique', 'unique(email)', 'L\'email doit être unique!'),
    ]

    def __str__(self):
        return f'{self.name} {self.prenom}'
