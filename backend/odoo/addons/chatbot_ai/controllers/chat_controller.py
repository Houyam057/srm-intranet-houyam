import json
import logging
from datetime import datetime

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)

try:
    from ..services.ai_service import AIService
except ImportError:
    AIService = None
    _logger.warning("AIService indisponible (openai non installé dans l'environnement Odoo)")


class ChatbotController(http.Controller):
    """API REST pour le chatbot IA."""

    def _response(self, data=None, error=None, status=200):
        response = {
            'success': error is None,
            'data': data,
            'error': error,
            'timestamp': datetime.now().isoformat(),
        }
        response_obj = request.make_response(
            json.dumps(response),
            headers={'Content-Type': 'application/json'},
        )
        response_obj.status_code = status
        return response_obj

    @http.route('/api/chat', auth='user', methods=['POST'], csrf=False, cors='*')
    def send_message(self):
        """Reçoit un message et retourne la réponse de l'IA."""
        try:
            data = request.get_json_data()
            if not data or not data.get('message', '').strip():
                return self._response(error='Le message ne peut pas être vide', status=400)

            user_message = data['message'].strip()
            conversation_id = data.get('conversation_id')

            Conversation = request.env['chatbot.conversation'].sudo()

            if conversation_id:
                conversation = Conversation.browse(conversation_id)
                if not conversation.exists() or conversation.user_id.id != request.env.uid:
                    conversation = Conversation.create({'user_id': request.env.uid})
            else:
                conversation = Conversation.create({'user_id': request.env.uid})

            history = conversation.get_messages()

            if AIService is None:
                return self._response(error='Service IA non disponible. Installez openai: pip install openai', status=503)

            ai_service = AIService(request.env)
            ai_response = ai_service.get_response(user_message, history=history)

            conversation.add_message('user', user_message)
            conversation.add_message('assistant', ai_response)

            return self._response(data={
                'response': ai_response,
                'conversation_id': conversation.id,
            })

        except Exception as e:
            _logger.exception("Erreur dans /api/chat")
            return self._response(error=str(e), status=500)

    @http.route('/api/chat/history', auth='user', methods=['GET'], csrf=False, cors='*')
    def get_history(self, conversation_id=None, limit=20):
        """Récupère l'historique des conversations de l'utilisateur."""
        try:
            Conversation = request.env['chatbot.conversation'].sudo()
            domain = [('user_id', '=', request.env.uid)]

            if conversation_id:
                conversation = Conversation.browse(int(conversation_id))
                if conversation.exists() and conversation.user_id.id == request.env.uid:
                    return self._response(data={
                        'conversation': {
                            'id': conversation.id,
                            'name': conversation.name,
                            'messages': conversation.get_messages(),
                            'created_at': conversation.created_at.isoformat() if conversation.created_at else None,
                            'updated_at': conversation.updated_at.isoformat() if conversation.updated_at else None,
                        }
                    })
                return self._response(error='Conversation non trouvée', status=404)

            conversations = Conversation.search(domain, limit=int(limit))
            return self._response(data={
                'conversations': [{
                    'id': c.id,
                    'name': c.name,
                    'message_count': c.message_count,
                    'created_at': c.created_at.isoformat() if c.created_at else None,
                    'updated_at': c.updated_at.isoformat() if c.updated_at else None,
                } for c in conversations]
            })

        except Exception as e:
            _logger.exception("Erreur dans /api/chat/history")
            return self._response(error=str(e), status=500)

    @http.route('/api/chat/conversation/<int:conversation_id>', auth='user', methods=['DELETE'], csrf=False, cors='*')
    def delete_conversation(self, conversation_id):
        """Supprime une conversation."""
        try:
            Conversation = request.env['chatbot.conversation'].sudo()
            conversation = Conversation.browse(conversation_id)

            if not conversation.exists() or conversation.user_id.id != request.env.uid:
                return self._response(error='Conversation non trouvée', status=404)

            conversation.unlink()
            return self._response(data={'deleted': True})

        except Exception as e:
            _logger.exception("Erreur dans /api/chat/conversation/delete")
            return self._response(error=str(e), status=500)
