from odoo import fields, models, api


class AccountPaymentLineCreate(models.TransientModel):
    _inherit = 'account.payment.line.create'

    date_type = fields.Selection(selection_add=[("date_range", "Date Range")], ondelete={"date_range": "cascade"})
    range_id = fields.Many2one('date.range', 'Period')

    def _prepare_move_line_domain(self):
        # inherit super
        domain = super(AccountPaymentLineCreate, self)._prepare_move_line_domain()
        if self.date_type == "date_range":
            domain += [
                ("date", ">=", self.range_id.date_start),
                ("date", "<=", self.range_id.date_end),
            ]
        return domain
