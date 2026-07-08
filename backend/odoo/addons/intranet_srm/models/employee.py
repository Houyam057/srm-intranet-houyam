from odoo import models, fields, api

class Employee(models.Model):
    _name = 'intranet.employee'
    _description = 'Employé'
    _rec_name = 'name'

    name = fields.Char('Nom', required=True)
    email = fields.Char('Email', required=True)
    phone = fields.Char('Téléphone')
    
    direction_id = fields.Many2one('intranet.direction', string='Direction', required=True)
    direction_name = fields.Char('Nom de la Direction', related='direction_id.name', store=True)
    
    job_title = fields.Char('Titre du Poste')
    avatar = fields.Binary('Avatar')
    avatar_url = fields.Char('URL Avatar')
    
    is_manager = fields.Boolean('Est Manager', default=False)
    manages_direction_id = fields.Many2one('intranet.direction', string='Gère la Direction')
    
    active = fields.Boolean('Actif', default=True)
    created_at = fields.Datetime('Date de création', default=fields.Datetime.now)

    _sql_constraints = [
        ('email_unique', 'unique(email)', 'L\'email doit être unique!'),
    ]

    def __str__(self):
        return self.name
