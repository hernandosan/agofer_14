from odoo import http
from odoo.addons.helpdesk_mgmt.controllers.main import HelpdeskTicketController


class CustomHelpdeskTicketController(HelpdeskTicketController):
    @http.route("/new/ticket", type="http", auth="user", website=True)
    def create_new_ticket(self, **kw):
        types = http.request.env["helpdesk.ticket.type"].search([])
        categories = http.request.env["helpdesk.ticket.category"].search([])
        email = http.request.env.user.email
        name = http.request.env.user.name
        return http.request.render(
            "helpdesk_mgmt.portal_create_ticket",
            {"email": email, "name": name, "categories": categories, "types": types},
        )

    @http.route("/nuevo/ticket", type="json", auth="user", website=True)
    def nuevo_ticket(self, team):
        categories = http.request.env["helpdesk.ticket.category"].search([("active", "=", True), ('team_id', '=', team)])
        category = []
        for record in categories:
            news = {
                "id": record.id,
                "name": record.name,
            }
            category.append(news)
        return category
