import logging

_logger = logging.getLogger(__name__)


def get_employee_info(env):
    """Récupère les informations de l'employé connecté."""
    user = env.user
    intranet_user = env['intranet.user'].sudo().search(
        [('res_user_id', '=', user.id)], limit=1
    )
    if not intranet_user:
        return {'error': 'Profil intranet non trouvé'}

    return {
        'name': intranet_user.name,
        'email': intranet_user.email or '',
        'phone': intranet_user.phone or '',
        'job_title': intranet_user.job_title or '',
        'direction_name': intranet_user.direction_name or '',
        'role': intranet_user.role or '',
        'is_manager': intranet_user.is_manager,
    }


def search_employee(env, name=''):
    """Recherche un employé par nom."""
    if not name:
        return {'error': 'Veuillez fournir un nom à rechercher'}

    User = env['intranet.user'].sudo()
    employees = User.search([
        ('name', 'ilike', name),
        ('active', '=', True),
    ], limit=10)

    if not employees:
        return {'results': [], 'message': f'Aucun employé trouvé pour "{name}"'}

    return {
        'results': [{
            'name': emp.name,
            'email': emp.email or '',
            'job_title': emp.job_title or '',
            'direction_name': emp.direction_name or '',
        } for emp in employees]
    }


def get_documents(env):
    """Liste les documents publics de l'intranet."""
    Document = env['intranet.document'].sudo()
    documents = Document.search([('public', '=', True)], limit=20)

    if not documents:
        return {'results': [], 'message': 'Aucun document public disponible'}

    return {
        'results': [{
            'name': doc.name,
            'description': doc.description or '',
            'category': doc.category or '',
            'file_type': doc.file_type or '',
        } for doc in documents]
    }


def get_news(env, limit=5):
    """Récupère les dernières actualités."""
    News = env['intranet.news'].sudo()
    news = News.search(
        [('published', '=', True)],
        order='published_date DESC',
        limit=int(limit)
    )

    if not news:
        return {'results': [], 'message': 'Aucune actualité disponible'}

    return {
        'results': [{
            'title': n.title,
            'summary': n.summary or '',
            'category': n.category or '',
            'published_date': n.published_date.isoformat() if n.published_date else '',
        } for n in news]
    }


def get_directions(env):
    """Liste les directions de l'entreprise."""
    Direction = env['intranet.direction'].sudo()
    directions = Direction.search([('active', '=', True)])

    if not directions:
        return {'results': [], 'message': 'Aucune direction trouvée'}

    return {
        'results': [{
            'name': d.name,
            'code': d.code or '',
            'manager_name': d.manager_name or '',
        } for d in directions]
    }


TOOLS_DEFINITIONS = [
    {
        'type': 'function',
        'function': {
            'name': 'get_employee_info',
            'description': 'Récupère les informations de l\'employé connecté (nom, email, poste, département, rôle).',
            'parameters': {
                'type': 'object',
                'properties': {},
                'required': [],
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'search_employee',
            'description': 'Recherche un employé par son nom dans l\'annuaire de l\'entreprise.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'name': {
                        'type': 'string',
                        'description': 'Nom ou partie du nom de l\'employé à rechercher'
                    }
                },
                'required': ['name']
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'get_documents',
            'description': 'Liste les documents publics disponibles sur l\'intranet (procédures, guides, policies).',
            'parameters': {
                'type': 'object',
                'properties': {},
                'required': []
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'get_news',
            'description': 'Récupère les dernières actualités et news de l\'entreprise.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'limit': {
                        'type': 'integer',
                        'description': 'Nombre d\'actualités à récupérer (défaut: 5)'
                    }
                },
                'required': []
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'get_directions',
            'description': 'Liste les directions/départements de l\'entreprise avec leurs responsables.',
            'parameters': {
                'type': 'object',
                'properties': {},
                'required': []
            }
        }
    },
]

TOOLS_MAP = {
    'get_employee_info': lambda env, **kw: get_employee_info(env),
    'search_employee': lambda env, **kw: search_employee(env, name=kw.get('name', '')),
    'get_documents': lambda env, **kw: get_documents(env),
    'get_news': lambda env, **kw: get_news(env, limit=kw.get('limit', 5)),
    'get_directions': lambda env, **kw: get_directions(env),
}
