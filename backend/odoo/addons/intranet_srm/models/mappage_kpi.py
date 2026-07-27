from odoo import models, fields

class MappageKpi(models.Model):
    _name = 'intranet.mappage_kpi'
    _description = 'Mappage KPI - Direction'
    _rec_name = 'display_name'

    direction_id = fields.Many2one('intranet.direction', string='Direction', required=True, ondelete='cascade')
    direction_name = fields.Char('Direction', related='direction_id.name', store=True)

    kpi_id = fields.Many2one('intranet.kpi', string='KPI', required=True, ondelete='cascade')
    kpi_name = fields.Char('KPI', related='kpi_id.name', store=True)

    display_name = fields.Char('Display Name', compute='_compute_display_name')

    _sql_constraints = [
        ('unique_direction_kpi', 'UNIQUE(direction_id, kpi_id)', 'Ce KPI est déjà affecté à cette direction.')
    ]

    def _compute_display_name(self):
        for record in self:
            record.display_name = f"{record.direction_name} - {record.kpi_name}"
