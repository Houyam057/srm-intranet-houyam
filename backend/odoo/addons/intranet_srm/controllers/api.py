import json
from odoo import http
from odoo.http import request
from datetime import datetime

class IntranetAPI(http.Controller):
    """API REST pour l'Intranet SRM-TTA"""

    def _response(self, data=None, error=None, status=200):
        """Helper pour retourner une réponse JSON cohérente"""
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

    # ===== DIRECTIONS =====
    @http.route('/api/directions', auth='public', methods=['GET'], csrf=False, cors='*')
    def get_directions(self):
        """Récupère toutes les directions"""
        try:
            Direction = request.env['intranet.direction'].sudo()
            directions = Direction.search([('active', '=', True)])
            
            data = [{
                'id': d.id,
                'name': d.name,
                'code': d.code,
                'manager_name': d.manager_name,
                'pole_name': d.pole_name,
                'employee_count': d.employee_count,
                'description': d.description,
            } for d in directions]
            
            return self._response(data={'directions': data})
        except Exception as e:
            return self._response(error=str(e), status=500)

    @http.route('/api/directions/<int:direction_id>', auth='public', methods=['GET'], csrf=False, cors='*')
    def get_direction(self, direction_id):
        """Récupère une direction spécifique"""
        try:
            Direction = request.env['intranet.direction'].sudo()
            direction = Direction.browse(direction_id)
            
            if not direction.exists():
                return self._response(error='Direction non trouvée', status=404)
            
            employees = [{
                'id': e.id,
                'name': e.name,
                'email': e.email,
                'phone': e.phone,
                'job_title': e.job_title,
            } for e in direction.employee_ids]
            
            data = {
                'id': direction.id,
                'name': direction.name,
                'code': direction.code,
                'manager_name': direction.manager_name,
                'pole_name': direction.pole_name,
                'employee_count': direction.employee_count,
                'description': direction.description,
                'employees': employees,
            }
            
            return self._response(data=data)
        except Exception as e:
            return self._response(error=str(e), status=500)

    @http.route('/api/directions', auth='user', methods=['POST'], csrf=False, cors='*')
    def create_direction(self):
        """Crée une nouvelle direction"""
        try:
            data = request.get_json_data()
            Direction = request.env['intranet.direction']
            
            new_direction = Direction.create({
                'name': data.get('name'),
                'code': data.get('code'),
                'pole_id': data.get('pole_id'),
                'description': data.get('description'),
            })
            
            return self._response(data={'id': new_direction.id, 'name': new_direction.name}, status=201)
        except Exception as e:
            return self._response(error=str(e), status=400)

    # ===== EMPLOYEES =====
    @http.route('/api/employees', auth='public', methods=['GET'], csrf=False, cors='*')
    def get_employees(self):
        """Récupère tous les employés"""
        try:
            Employee = request.env['intranet.employee'].sudo()
            employees = Employee.search([('active', '=', True)])
            
            data = [{
                'id': e.id,
                'name': e.name,
                'email': e.email,
                'phone': e.phone,
                'job_title': e.job_title,
                'direction_name': e.direction_name,
                'is_manager': e.is_manager,
            } for e in employees]
            
            return self._response(data={'employees': data})
        except Exception as e:
            return self._response(error=str(e), status=500)

    @http.route('/api/employees/<int:employee_id>', auth='public', methods=['GET'], csrf=False, cors='*')
    def get_employee(self, employee_id):
        """Récupère un employé spécifique"""
        try:
            Employee = request.env['intranet.employee'].sudo()
            employee = Employee.browse(employee_id)
            
            if not employee.exists():
                return self._response(error='Employé non trouvé', status=404)
            
            data = {
                'id': employee.id,
                'name': employee.name,
                'email': employee.email,
                'phone': employee.phone,
                'job_title': employee.job_title,
                'direction_name': employee.direction_name,
                'is_manager': employee.is_manager,
                'avatar_url': employee.avatar_url,
            }
            
            return self._response(data=data)
        except Exception as e:
            return self._response(error=str(e), status=500)

    # ===== NEWS / ACTUALITÉS =====
    @http.route('/api/news', auth='public', methods=['GET'], csrf=False, cors='*')
    def get_news(self, limit=10):
        """Récupère les actualités récentes"""
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
        """Récupère une actualité spécifique"""
        try:
            News = request.env['intranet.news'].sudo()
            news = News.browse(news_id)
            
            if not news.exists():
                return self._response(error='Actualité non trouvée', status=404)
            
            # Incrémenter le nombre de vues
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
        """Crée une nouvelle actualité"""
        try:
            data = request.get_json_data()
            News = request.env['intranet.news']
            
            new_news = News.create({
                'title': data.get('title'),
                'content': data.get('content'),
                'summary': data.get('summary'),
                'author_id': getattr(request.env.user, 'employee_id', False).id if getattr(request.env.user, 'employee_id', False) else False,
                'priority': data.get('priority', 'medium'),
                'category': data.get('category', 'Actualité'),
            })
            
            return self._response(data={'id': new_news.id, 'title': new_news.title}, status=201)
        except Exception as e:
            return self._response(error=str(e), status=400)

    # ===== DOCUMENTS =====
    @http.route('/api/documents', auth='public', methods=['GET'], csrf=False, cors='*')
    def get_documents(self):
        """Récupère tous les documents"""
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
        """Télécharge un document"""
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
        """Crée un nouveau feedback"""
        try:
            data = request.get_json_data()
            Feedback = request.env['intranet.feedback']
            
            new_feedback = Feedback.create({
                'employee_id': getattr(request.env.user, 'employee_id', False).id if getattr(request.env.user, 'employee_id', False) else False,
                'mood': data.get('mood'),
                'comment': data.get('comment'),
                'category': data.get('category', 'Général'),
                'anonymous': data.get('anonymous', False),
            })
            
            return self._response(data={'id': new_feedback.id}, status=201)
        except Exception as e:
            return self._response(error=str(e), status=400)

    @http.route('/api/feedback/stats', auth='public', methods=['GET'], csrf=False, cors='*')
    def get_feedback_stats(self):
        """Récupère les statistiques de feedback"""
        try:
            Feedback = request.env['intranet.feedback'].sudo()
            stats = Feedback.get_mood_stats()
            return self._response(data={'stats': stats})
        except Exception as e:
            return self._response(error=str(e), status=500)

    # ===== DASHBOARD =====
    @http.route('/api/dashboard', auth='public', methods=['GET'], csrf=False, cors='*')
    def get_dashboard(self):
        """Récupère les données du dashboard"""
        try:
            Direction = request.env['intranet.direction'].sudo()
            Employee = request.env['intranet.employee'].sudo()
            News = request.env['intranet.news'].sudo()
            
            data = {
                'total_directions': Direction.search_count([('active', '=', True)]),
                'total_employees': Employee.search_count([('active', '=', True)]),
                'recent_news': [{
                    'id': n.id,
                    'title': n.title,
                    'published_date': n.published_date.isoformat() if n.published_date else None,
                } for n in News.search([('published', '=', True)], order='published_date DESC', limit=5)],
            }
            
            return self._response(data=data)
        except Exception as e:
            return self._response(error=str(e), status=500)
