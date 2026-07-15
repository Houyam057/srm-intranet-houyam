from odoo import models, fields, api


class User(models.Model):
    _name = 'intranet.user'
    _description = 'Utilisateur Intranet'
    _rec_name = 'name'
    _auto = False
    _table = 'intranet_user'

    ROLE_SELECTION = [
        ('user', 'Utilisateur'),
        ('admin', 'Administrateur'),
    ]

    id = fields.Id('ID', readonly=True)
    name = fields.Char('Nom', readonly=True)
    email = fields.Char('Email', readonly=True)
    phone = fields.Char('Téléphone', readonly=True)
    login = fields.Char('Login', readonly=True)
    role = fields.Selection(ROLE_SELECTION, string='Rôle', readonly=True)
    direction_id = fields.Integer('Direction ID')
    direction_name = fields.Char('Direction', readonly=True)
    job_title = fields.Char('Titre du Poste', readonly=True)
    is_manager = fields.Boolean('Est Manager', readonly=True)
    manages_direction_id = fields.Integer('Gère la Direction ID')
    avatar_url = fields.Char('URL Avatar', readonly=True)
    active = fields.Boolean('Actif', readonly=True)
    created_at = fields.Datetime('Date de création', readonly=True)
