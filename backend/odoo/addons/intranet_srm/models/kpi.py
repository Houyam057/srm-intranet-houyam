from odoo import api, models, fields

class Kpi(models.Model):
    _name = 'intranet.kpi'
    _description = 'KPI'
    _rec_name = 'name'

    name = fields.Char('Nom', required=True)
    val = fields.Float('Valeur')

    mappage_ids = fields.One2many('intranet.mappage_kpi', 'kpi_id', string='Mappages')
    direction_count = fields.Integer('Nombre de Directions', compute='_compute_direction_count', store=True)

    active = fields.Boolean('Actif', default=True)
    created_at = fields.Datetime('Date de création', default=fields.Datetime.now)

    @api.depends('mappage_ids')
    def _compute_direction_count(self):
        for record in self:
            record.direction_count = len(record.mappage_ids)
