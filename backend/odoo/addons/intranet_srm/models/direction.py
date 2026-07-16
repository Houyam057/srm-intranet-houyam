from odoo import models, fields, api

class Direction(models.Model):
    _name = 'intranet.direction'
    _description = 'Direction'
    _rec_name = 'name'

    name = fields.Char('Nom de la Direction', required=True)
    code = fields.Char('Code')
    manager_id = fields.Many2one('intranet.user', string='Manager')
    manager_name = fields.Char('Nom du Manager', related='manager_id.name', store=True)

    pole_id = fields.Many2one('intranet.pole', string='Pôle')
    pole_name = fields.Char('Nom du Pôle', related='pole_id.name', store=True)

    employee_ids = fields.One2many('intranet.user', 'direction_id', string='Employés')
    employee_count = fields.Integer('Nombre d\'employés', compute='_compute_employee_count', store=True)
    
    description = fields.Text('Description')
    active = fields.Boolean('Actif', default=True)
    
    created_at = fields.Datetime('Date de création', default=fields.Datetime.now)
    updated_at = fields.Datetime('Dernière mise à jour', compute='_compute_updated_at', store=True)

    @api.depends('employee_ids')
    def _compute_employee_count(self):
        for record in self:
            record.employee_count = len(record.employee_ids)

    @api.depends('write_date')
    def _compute_updated_at(self):
        for record in self:
            record.updated_at = record.write_date or record.create_date

    def __str__(self):
        return self.name

    _sql_constraints = [
        ('code_unique', 'unique(code)', 'Le code doit être unique!'),
    ]
