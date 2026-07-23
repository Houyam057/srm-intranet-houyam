from odoo import models, fields, api


ADMIN_JOBS = ['directeur', 'chef_departement', 'chef_division', 'chef_service']


class User(models.Model):
    _name = 'intranet.user'
    _description = 'Utilisateur Intranet'
    _rec_name = 'name'

    ROLE_SELECTION = [
        ('user', 'Utilisateur'),
        ('admin', 'Administrateur'),
    ]

    JOB_SELECTION = [
        ('directeur', 'Directeur'),
        ('chef_departement', 'Chef Département'),
        ('chef_division', 'Chef Division'),
        ('chef_service', 'Chef Service'),
        ('cadre', 'Cadre'),
        ('technicien', 'Technicien'),
    ]

    name = fields.Char('Nom')
    email = fields.Char('Email')
    phone = fields.Char('Téléphone')
    login = fields.Char('Login')
    role = fields.Selection(ROLE_SELECTION, string='Rôle', readonly=True)
    direction_id = fields.Many2one('intranet.direction', string='Direction')
    direction_name = fields.Char('Direction Nom', related='direction_id.name', store=True)
    job_title = fields.Selection(JOB_SELECTION, string='Poste')
    is_manager = fields.Boolean('Est Manager')
    manages_direction_id = fields.Integer('Gère la Direction ID')
    avatar_url = fields.Char('URL Avatar')
    active = fields.Boolean('Actif', default=True)
    created_at = fields.Datetime('Date de création', readonly=True, default=fields.Datetime.now)
    res_user_id = fields.Many2one('res.users', string='Compte Odoo', readonly=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            role = 'admin' if vals.get('job_title') in ADMIN_JOBS else 'user'
            vals['role'] = role

            login = vals.get('login') or vals.get('email')
            res_user = self.env['res.users'].sudo().create({
                'name': vals.get('name', ''),
                'login': login,
                'email': vals.get('email', ''),
                'phone': vals.get('phone', ''),
                'password': 'admin',
            })
            vals['res_user_id'] = res_user.id

        return super().create(vals_list)
