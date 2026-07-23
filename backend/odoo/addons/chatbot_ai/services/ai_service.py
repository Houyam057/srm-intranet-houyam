import json
import logging

_logger = logging.getLogger(__name__)

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None
    _logger.warning("Le module 'openai' n'est pas installé. pip install openai")

from .tools import TOOLS_DEFINITIONS, TOOLS_MAP

SYSTEM_PROMPT = """Tu es un assistant IA intégré à l'intranet de l'entreprise SRM-TTA.
Tu assistes les employés dans leurs questions quotidiennes.

Règles à respecter:
- Réponds toujours en français, sauf si l'utilisateur te parle dans une autre langue.
- Sois courtois, professionnel et concis.
- Si tu ne connais pas la réponse, dis-le honnêtement.
- Tu peux utiliser les outils mis à disposition pour consulter les données de l'entreprise.
- Ne invente jamais d'informations sur les employés, congés, ou données internes.
- Pour les demandes d'action (créer un congé, un ticket, etc.), explique la procédure à suivre
  car tu ne peux pas encore créer ces éléments directement.
- Adapte ton ton au contexte: formel pour les questions RH, direct pour les questions techniques.
"""


class AIService:
    """Service d'intégration IA pour le chatbot."""

    def __init__(self, env):
        self.env = env
        self._client = None

    def _get_param(self, key, default=None):
        Parameter = self.env['ir.config_parameter'].sudo()
        return Parameter.get_param(key, default or '')

    def _get_api_key(self):
        return self._get_param('chatbot.ai_api_key') or self._get_param('chatbot.openai_api_key')

    def _get_base_url(self):
        return self._get_param('chatbot.ai_base_url', 'https://api.groq.com/openai/v1')

    def _get_model(self):
        return self._get_param('chatbot.ai_model', 'llama-3.1-8b-instant')

    @property
    def client(self):
        if self._client is None:
            api_key = self._get_api_key()
            if not api_key:
                return None
            if OpenAI is None:
                return None
            self._client = OpenAI(
                api_key=api_key,
                base_url=self._get_base_url(),
            )
        return self._client

    def _build_user_context(self):
        user = self.env.user
        context_lines = [
            f"Nom: {user.name}",
            f"Email: {user.email or 'N/A'}",
        ]
        try:
            intranet_user = self.env['intranet.user'].sudo().search(
                [('res_user_id', '=', user.id)], limit=1
            )
            if intranet_user and intranet_user.exists():
                context_lines.extend([
                    f"Poste: {intranet_user.job_title or 'N/A'}",
                    f"Département: {intranet_user.direction_name or 'N/A'}",
                    f"Rôle: {'Manager' if intranet_user.is_manager else 'Employé'}",
                ])
        except Exception:
            pass
        return "\n".join(context_lines)

    def _execute_tool(self, tool_name, tool_args):
        tool_fn = TOOLS_MAP.get(tool_name)
        if not tool_fn:
            return {'error': f'Outil inconnu: {tool_name}'}
        try:
            return tool_fn(self.env, **tool_args)
        except Exception as e:
            _logger.exception("Erreur lors de l'exécution de l'outil %s", tool_name)
            return {'error': str(e)}

    def get_response(self, user_message, history=None):
        if not self.client:
            return "Désolé, le service IA n'est pas configuré. Veuillez contacter l'administrateur."

        model = self._get_model()
        user_context = self._build_user_context()

        messages = [
            {
                'role': 'system',
                'content': f"{SYSTEM_PROMPT}\n\n---\nInformations sur l'utilisateur:\n{user_context}"
            }
        ]

        if history:
            messages.extend(history)

        messages.append({'role': 'user', 'content': user_message})

        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                tools=TOOLS_DEFINITIONS,
                tool_choice='auto',
                max_tokens=1024,
                temperature=0.7,
            )

            assistant_message = response.choices[0].message

            if assistant_message.tool_calls:
                messages.append({
                    'role': 'assistant',
                    'content': assistant_message.content or '',
                    'tool_calls': [
                        {
                            'id': tc.id,
                            'type': 'function',
                            'function': {
                                'name': tc.function.name,
                                'arguments': tc.function.arguments,
                            }
                        } for tc in assistant_message.tool_calls
                    ],
                })

                for tool_call in assistant_message.tool_calls:
                    fn_name = tool_call.function.name
                    try:
                        fn_args = json.loads(tool_call.function.arguments)
                    except json.JSONDecodeError:
                        fn_args = {}

                    _logger.info("Exécution de l'outil: %s(%s)", fn_name, fn_args)
                    result = self._execute_tool(fn_name, fn_args)

                    messages.append({
                        'role': 'tool',
                        'tool_call_id': tool_call.id,
                        'content': json.dumps(result, ensure_ascii=False),
                    })

                second_response = self.client.chat.completions.create(
                    model=model,
                    messages=messages,
                    max_tokens=1024,
                    temperature=0.7,
                )

                return second_response.choices[0].message.content

            return assistant_message.content

        except Exception as e:
            _logger.exception("Erreur lors de l'appel à l'IA")
            return f"Une erreur est survenue: {str(e)}"
