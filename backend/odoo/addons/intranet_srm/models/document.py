from odoo import models, fields, api
import base64

class Document(models.Model):
    _name = 'intranet.document'
    _description = 'Document'
    _rec_name = 'name'
    _order = 'created_at DESC'

    FILE_TYPES = [
        ('pdf', 'PDF'),
        ('docx', 'Word'),
        ('pptx', 'Présentation'),
        ('xlsx', 'Excel'),
        ('other', 'Autre'),
    ]

    name = fields.Char('Nom du document', required=True)
    description = fields.Text('Description')
    
    file = fields.Binary('Fichier', required=True)
    file_name = fields.Char('Nom du fichier')
    file_type = fields.Selection(FILE_TYPES, string='Type de fichier', required=True)
    file_size = fields.Integer('Taille (bytes)')
    
    direction_id = fields.Many2one('intranet.direction', string='Direction')
    uploader_id = fields.Many2one('intranet.user', string='Uploader')
    
    category = fields.Char('Catégorie', default='Général')
    public = fields.Boolean('Public', default=True)
    
    created_at = fields.Datetime('Date de création', default=fields.Datetime.now)
    updated_at = fields.Datetime('Dernière mise à jour')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if 'file' in vals and vals['file']:
                # Calcul de la taille du fichier
                file_data = vals['file']
                if isinstance(file_data, str):
                    vals['file_size'] = len(base64.b64decode(file_data))
                else:
                    vals['file_size'] = len(file_data)
        return super().create(vals_list)

    def get_file_size_mb(self):
        """Retourne la taille en MB"""
        if self.file_size:
            return round(self.file_size / (1024 * 1024), 1)
        return 0

    def __str__(self):
        return self.name
