{
    'name': 'Chatbot AI',
    'version': '19.0.1.0.0',
    'category': 'Tools',
    'summary': 'Assistant IA pour l\'intranet',
    'description': """
        Assistant IA integre a l'intranet base sur OpenAI.
    """,
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/conversation_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
