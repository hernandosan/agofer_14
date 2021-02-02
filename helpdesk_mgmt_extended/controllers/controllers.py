from odoo import http
from odoo.addons.helpdesk_mgmt.controllers.main import HelpdeskTicketController


class CustomHelpdeskTicketController(HelpdeskTicketController):
    @http.route("/new/ticket", type="http", auth="user", website=True)
    def create_new_ticket(self, **kw):
        categories = http.request.env["helpdesk.ticket.category"].search(
            [("active", "=", True), ('team_id', '=', )])
        types = http.request.env["helpdesk.ticket.type"].search([])
        email = http.request.env.user.email
        name = http.request.env.user.name
        return http.request.render(
            "helpdesk_mgmt.portal_create_ticket",
            {"categories": categories, "email": email, "name": name, "types": types},
        )
