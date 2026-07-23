import json
import logging
from odoo import http
from odoo.http import request
from datetime import datetime

_logger = logging.getLogger(__name__)


class IntranetAPI(http.Controller):
    """API REST pour l'Intranet SRM-TTA"""

    def _response(self, data=None, error=None, status=200):
        response = {
            'success': error is None,
            'data': data,
            'error': error,
            'timestamp': datetime.now().isoformat()
        }
        response_obj = request.make_response(
            json.dumps(response),
            headers={'Content-Type': 'application/json'}
        )
        response_obj.status_code = status
        return response_obj

    def _missing_fields(self, data, required):
        """Return the names of required keys that are absent or empty in data."""
        return [f for f in required if not data.get(f)]

    def _server_error(self, e, status=500):
        """Log the real exception server-side; never echo internal details to the client."""
        _logger.exception("API error")
        return self._response(error="Une erreur interne est survenue.", status=status)

    # ===== USER =====
    @http.route('/api/user/me', auth='user', methods=['GET'], csrf=False, cors='*')
    def get_current_user(self):
        """Get the intranet.user for the logged-in Odoo user"""
        try:
            odoo_user = request.env.user
            if not odoo_user or not odoo_user.exists():
                return self._response(error='Utilisateur non trouvé', status=404)

            User = request.env['intranet.user'].sudo()
            user = User.search([('res_user_id', '=', odoo_user.id)], limit=1)
            if not user.exists():
                return self._response(error='Utilisateur non trouvé', status=404)

            data = {
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'phone': user.phone or '',
                'role': user.role,
                'direction_id': user.direction_id.id if user.direction_id else 0,
                'job_title': user.job_title or '',
                'is_manager': user.is_manager,
                'avatar_url': user.avatar_url or '',
                'direction_name': user.direction_name or '',
            }
            return self._response(data=data)
        except Exception as e:
            return self._response(error=str(e), status=500)

    # ===== DIRECTIONS =====
    @http.route('/api/directions', auth='public', methods=['GET'], csrf=False, cors='*')
    def get_directions(self):
        try:
            Direction = request.env['intranet.direction'].sudo()
<<<<<<< HEAD
=======
            User = request.env['intranet.user'].sudo()
>>>>>>> c8f87b30f6980ce158dc783bf164985484c47d2a
            directions = Direction.search([('active', '=', True)])

            data = [{
                'id': d.id,
                'name': d.name,
                'code': d.code or '',
                'manager_name': d.manager_name,
<<<<<<< HEAD
                'pole_name': d.pole_id.name if d.pole_id else '',
                'pole_manager_name': d.pole_id.manager_name if d.pole_id else '',
=======
                'pole_name': d.pole_id.name or '',
                'direction_p_name': d.direction_p_name,
                'employee_count': User.search_count([('direction_id', '=', d.id)]),
>>>>>>> c8f87b30f6980ce158dc783bf164985484c47d2a
                'description': d.description,
            } for d in directions]

            return self._response(data={'directions': data})
        except Exception as e:
            return self._response(error=str(e), status=500)

    @http.route('/api/directions/<int:direction_id>', auth='public', methods=['GET'], csrf=False, cors='*')
    def get_direction(self, direction_id):
        try:
            Direction = request.env['intranet.direction'].sudo()
<<<<<<< HEAD
=======
            User = request.env['intranet.user'].sudo()
>>>>>>> c8f87b30f6980ce158dc783bf164985484c47d2a
            direction = Direction.browse(direction_id)

            if not direction.exists():
                return self._response(error='Direction non trouvée', status=404)

            employees = [{
                'id': e.id,
                'name': e.name,
                'email': e.email,
                'phone': e.phone,
                'job_title': e.job_title,
            } for e in User.search([('direction_id', '=', direction.id)])]

            data = {
                'id': direction.id,
                'name': direction.name,
                'code': direction.code or '',
                'manager_name': direction.manager_name,
<<<<<<< HEAD
                'pole_name': direction.pole_id.name if direction.pole_id else '',
                'pole_manager_name': direction.pole_id.manager_name if direction.pole_id else '',
=======
                'pole_name': direction.pole_id.name or '',
                'direction_p_name': direction.direction_p_name,
                'employee_count': len(employees),
>>>>>>> c8f87b30f6980ce158dc783bf164985484c47d2a
                'description': direction.description,
            }

            return self._response(data=data)
        except Exception as e:
            return self._response(error=str(e), status=500)

    @http.route('/api/directions', auth='user', methods=['POST'], csrf=False, cors='*')
    def create_direction(self):
        try:
            data = request.get_json_data()
<<<<<<< HEAD
            Direction = request.env['intranet.direction']
=======
            missing = self._missing_fields(data, ['name'])
            if missing:
                return self._response(error=f"Champs requis manquants : {', '.join(missing)}", status=400)
>>>>>>> c8f87b30f6980ce158dc783bf164985484c47d2a

            Direction = request.env['intranet.direction']
            new_direction = Direction.create({
                'name': data.get('name'),
                'code': data.get('code'),
                'description': data.get('description'),
                'manager_id': data.get('manager_id'),
                'pole_id': data.get('pole_id'),
                'direction_p_id': data.get('direction_p_id'),
            })

            return self._response(data={'id': new_direction.id, 'name': new_direction.name}, status=201)
        except Exception as e:
            return self._server_error(e, status=400)

    # ===== EMPLOYEES =====
    @http.route('/api/employees', auth='public', methods=['GET'], csrf=False, cors='*')
    def get_employees(self):
        try:
            request.env.cr.execute("""
                SELECT u.id, u.name, u.email, u.phone, u.login, u.role,
                       u.direction_id, COALESCE(d.name, '') as direction_name,
                       u.job_title, u.is_manager, u.active, u.created_at
                FROM intranet_user u
                LEFT JOIN intranet_direction d ON u.direction_id = d.id
            """)
            columns = [desc[0] for desc in request.env.cr.description]
            rows = request.env.cr.fetchall()

            data = []
            for row in rows:
                r = dict(zip(columns, row))
                data.append({
                    'id': r['id'] or 0,
                    'name': r['name'] or '',
                    'email': r['email'] or '',
                    'phone': r['phone'] or '',
                    'login': r['login'] or '',
                    'role': r['role'] or '',
                    'direction_name': r['direction_name'] or '',
                    'job_title': r['job_title'] or '',
                    'is_manager': bool(r['is_manager']),
                    'active': bool(r['active']),
                    'created_at': str(r['created_at']) if r['created_at'] else '',
                })

            return self._response(data={'employees': data})
        except Exception as e:
            return self._response(error=str(e), status=500)

    @http.route('/api/employees/<int:employee_id>', auth='public', methods=['GET'], csrf=False, cors='*')
    def get_employee(self, employee_id):
        try:
            request.env.cr.execute("""
                SELECT u.*, COALESCE(d.name, '') as direction_name
                FROM intranet_user u
                LEFT JOIN intranet_direction d ON u.direction_id = d.id
                WHERE u.id = %s
            """, (employee_id,))
            columns = [desc[0] for desc in request.env.cr.description]
            row = request.env.cr.fetchone()

            if not row:
                return self._response(error='Employé non trouvé', status=404)

            r = dict(zip(columns, row))
            data = {
                'id': r.get('id') or 0,
                'name': r.get('name') or '',
                'email': r.get('email') or '',
                'phone': r.get('phone') or '',
                'login': r.get('login') or '',
                'role': r.get('role') or '',
                'direction_name': r.get('direction_name') or '',
                'job_title': r.get('job_title') or '',
                'is_manager': bool(r.get('is_manager')),
                'active': bool(r.get('active', True)),
                'created_at': str(r.get('created_at') or ''),
            }

            return self._response(data=data)
        except Exception as e:
            return self._response(error=str(e), status=500)

    # ===== NEWS =====
    @http.route('/api/news', auth='public', methods=['GET'], csrf=False, cors='*')
    def get_news(self, limit=10):
        try:
            News = request.env['intranet.news'].sudo()
            news = News.search([('published', '=', True)], order='published_date DESC', limit=int(limit))

            data = [{
                'id': n.id,
                'title': n.title,
                'summary': n.summary,
                'content': n.content,
                'image_url': n.image_url,
                'author_name': n.author_name,
                'priority': n.priority,
                'category': n.category,
                'published_date': n.published_date.isoformat() if n.published_date else None,
                'view_count': n.view_count,
            } for n in news]

            return self._response(data={'news': data})
        except Exception as e:
            return self._response(error=str(e), status=500)

    @http.route('/api/news/<int:news_id>', auth='public', methods=['GET'], csrf=False, cors='*')
    def get_news_detail(self, news_id):
        try:
            News = request.env['intranet.news'].sudo()
            news = News.browse(news_id)

            if not news.exists():
                return self._response(error='Actualité non trouvée', status=404)

            news.write({'view_count': news.view_count + 1})

            data = {
                'id': news.id,
                'title': news.title,
                'content': news.content,
                'summary': news.summary,
                'image_url': news.image_url,
                'author_name': news.author_name,
                'priority': news.priority,
                'category': news.category,
                'published_date': news.published_date.isoformat() if news.published_date else None,
                'view_count': news.view_count,
            }

            return self._response(data=data)
        except Exception as e:
            return self._response(error=str(e), status=500)

    @http.route('/api/news', auth='user', methods=['POST'], csrf=False, cors='*')
    def create_news(self):
        try:
            data = request.get_json_data()
            missing = self._missing_fields(data, ['title'])
            if missing:
                return self._response(error=f"Champs requis manquants : {', '.join(missing)}", status=400)

            News = request.env['intranet.news']
            new_news = News.create({
                'title': data.get('title'),
                'content': data.get('content'),
                'summary': data.get('summary'),
                'author_id': request.env.user.id,
                'priority': data.get('priority', 'medium'),
                'category': data.get('category', 'Actualité'),
            })

            return self._response(data={'id': new_news.id, 'title': new_news.title}, status=201)
        except Exception as e:
            return self._server_error(e, status=400)

    # ===== DOCUMENTS =====
    @http.route('/api/documents', auth='public', methods=['GET'], csrf=False, cors='*')
    def get_documents(self):
        try:
            Document = request.env['intranet.document'].sudo()
            documents = Document.search([('public', '=', True)])

            data = [{
                'id': d.id,
                'name': d.name,
                'description': d.description,
                'file_type': d.file_type,
                'file_size': f"{d.get_file_size_mb()} Mo",
                'category': d.category,
                'created_at': d.created_at.isoformat() if d.created_at else None,
            } for d in documents]

            return self._response(data={'documents': data})
        except Exception as e:
            return self._response(error=str(e), status=500)

    @http.route('/api/documents/<int:document_id>/download', auth='public', methods=['GET'], csrf=False, cors='*')
    def download_document(self, document_id):
        try:
            Document = request.env['intranet.document'].sudo()
            document = Document.browse(document_id)

            if not document.exists():
                return self._response(error='Document non trouvé', status=404)

            response = request.make_response(document.file, headers=[
                ('Content-Type', 'application/octet-stream'),
                ('Content-Disposition', f'attachment; filename="{document.file_name}"')
            ])
            return response
        except Exception as e:
            return self._response(error=str(e), status=500)

    # ===== FEEDBACK =====
    @http.route('/api/feedback', auth='user', methods=['POST'], csrf=False, cors='*')
    def create_feedback(self):
        try:
            data = request.get_json_data()
            missing = self._missing_fields(data, ['mood'])
            if missing:
                return self._response(error=f"Champs requis manquants : {', '.join(missing)}", status=400)

            Feedback = request.env['intranet.feedback']
            new_feedback = Feedback.create({
                'employee_id': request.env.user.id,
                'mood': data.get('mood'),
                'comment': data.get('comment'),
                'category': data.get('category', 'Général'),
                'anonymous': data.get('anonymous', False),
            })

            return self._response(data={'id': new_feedback.id}, status=201)
        except Exception as e:
            return self._server_error(e, status=400)

    @http.route('/api/feedback/stats', auth='public', methods=['GET'], csrf=False, cors='*')
    def get_feedback_stats(self):
        try:
            Feedback = request.env['intranet.feedback'].sudo()
            stats = Feedback.get_mood_stats()
            return self._response(data={'stats': stats})
        except Exception as e:
            return self._response(error=str(e), status=500)

    # ===== EMAILS =====
    @http.route('/api/emails', auth='user', methods=['GET'], csrf=False, cors='*')
    def get_emails(self):
        try:
            uid = request.env.uid
            user = request.env['res.users'].sudo().browse(uid)
            partner_id = user.partner_id.id

            request.env.cr.execute("""
                SELECT DISTINCT model FROM mail_message WHERE model IS NOT NULL
            """)
            models = [r[0] for r in request.env.cr.fetchall()]

            def _fetch_messages(query, params):
                request.env.cr.execute(query, params)
                columns = [desc[0] for desc in request.env.cr.description]
                rows = request.env.cr.fetchall()
                result = []
                for row in rows:
                    r = dict(zip(columns, row))
                    body = r['body'] or ''
                    body_clean = body.replace('<p>', '').replace('</p>', '').replace('<br>', '').replace('<br/>', '').strip()
                    result.append({
                        'id': r['id'],
                        'subject': r['subject'] or '(Sans objet)',
                        'body': body_clean[:200],
                        'author_name': r['author_name'],
                        'author_email': r['author_email'],
                        'message_type': r['message_type'] or '',
                        'model': r['model'] or '',
                        'date': r['date'].isoformat() if r['date'] else '',
                        'is_read': False,
                    })
                return result

            base_query = """
                SELECT m.id, m.subject, m.body, m.date, m.message_type, m.model,
                       COALESCE(p.name, 'Inconnu') AS author_name,
                       COALESCE(p.email, '') AS author_email
                FROM mail_message m
                LEFT JOIN res_partner p ON m.author_id = p.id
                WHERE m.author_id != %s
            """

            emails = _fetch_messages(
                base_query + " AND COALESCE(m.message_type, '') NOT IN ('email_outgoing', 'notification') ORDER BY m.date DESC LIMIT 50",
                (int(partner_id),)
            )

            notifications = _fetch_messages(
                base_query + " AND COALESCE(m.message_type, '') IN ('email_outgoing', 'notification') ORDER BY m.date DESC LIMIT 50",
                (int(partner_id),)
            )

            return self._response(data={'emails': emails, 'notifications': notifications, 'models': models})
        except Exception as e:
            return self._response(error=str(e), status=500)

    @http.route('/api/emails/<int:email_id>/read', auth='user', methods=['PUT'], csrf=False, cors='*')
    def mark_email_read(self, email_id):
        try:
            Message = request.env['mail.message'].sudo()
            msg = Message.browse(email_id)
            if not msg.exists():
                return self._response(error='Message non trouvé', status=404)

            partner_id = request.env.user.partner_id.id
            notification = request.env['mail.notification'].sudo().search([
                ('mail_message_id', '=', email_id),
                ('res_partner_id', '=', partner_id),
            ], limit=1)
            if notification:
                notification.write({'is_read': True})

            return self._response(data={'id': email_id, 'is_read': True})
        except Exception as e:
            return self._server_error(e)

    # ===== HELPDESK =====
    @http.route('/api/tickets', auth='user', methods=['POST'], csrf=False, cors='*')
    def create_ticket(self):
        try:
            data = request.get_json_data()
            missing = self._missing_fields(data, ['subject', 'message'])
            if missing:
                return self._response(error=f"Champs requis manquants : {', '.join(missing)}", status=400)

            Ticket = request.env['intranet.helpdesk_ticket']
            vals = {
                'subject': data.get('subject'),
                'category': data.get('category'),
                'message': data.get('message'),
            }
            # employee_id pointe vers intranet.user, pas res.users : ne le renseigner
            # que si un enregistrement intranet.user existe vraiment pour cet id,
            # sinon la vue liste plante en essayant d'afficher un lien mort.
            employee = request.env['intranet.user'].sudo().browse(request.env.user.id)
            if employee.exists():
                vals['employee_id'] = employee.id
            new_ticket = Ticket.create(vals)

            return self._response(data={'id': new_ticket.id, 'status': new_ticket.status}, status=201)
        except Exception as e:
            return self._server_error(e, status=400)

    # ===== DASHBOARD =====
    @http.route('/api/dashboard', auth='public', methods=['GET'], csrf=False, cors='*')
    def get_dashboard(self):
        try:
            Direction = request.env['intranet.direction'].sudo()
            User = request.env['intranet.user'].sudo()
            News = request.env['intranet.news'].sudo()

            data = {
                'total_directions': Direction.search_count([('active', '=', True)]),
                'total_employees': User.search_count([('role', '=', 'user'), ('active', '=', True)]),
                'recent_news': [{
                    'id': n.id,
                    'title': n.title,
                    'published_date': n.published_date.isoformat() if n.published_date else None,
                } for n in News.search([('published', '=', True)], order='published_date DESC', limit=5)],
            }

            return self._response(data=data)
        except Exception as e:
            return self._response(error=str(e), status=500)
