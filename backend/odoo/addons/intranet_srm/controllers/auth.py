from odoo import http
from odoo.http import request


class AuthController(http.Controller):

    @http.route(
        "/api/test",
        type="json",
        auth="public",
        methods=["POST"]
    )
    def test(self):

        return {
            "message": "API Odoo fonctionne"
        }