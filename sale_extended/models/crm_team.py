# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class CrmTeam(models.Model):
    _inherit = 'crm.team'

    # CRM Team
    kilogram_target = fields.Float('Kilogram Target')
    kilogram = fields.Float('Kilogram Invoiced This Month', compute='_compute_kilogram', readonly=True)
    members_ids = fields.Many2many('res.users', 'team_user_rel', 'team_id', 'user_id', 'Members', 
        check_company=True, domain=[('share', '=', False)])
    # Account
    crossover_journal_id = fields.Many2one('account.journal', 'Crossover Journal', domain=[('type','in',('bank','cash'))])
    advance_journal_id = fields.Many2one('account.journal', 'Advance Journal', domain=[('type','in',('bank','cash'))])
    advance_account_id = fields.Many2one('account.account', 'Advance Account', domain=[('user_type_id.type','=','payable')])
    # Pricelist
    pricelists_ids = fields.Many2many('product.pricelist', string='Pricelists')
    # Stock
    warehouses_ids = fields.Many2many('stock.warehouse', string='Warehouses')

    def _team_crossover_journal(self):
        self.ensure_one()
        if not self.crossover_journal_id:
            raise ValidationError(_("The CRM Team %s has not crossover journal") % self.name)
        return self.crossover_journal_id

    def _team_advance_journal(self):
        self.ensure_one()
        if not self.advance_journal_id:
            raise ValidationError(_("The CRM Team %s has not advance journal") % self.name)
        return self.crossover_journal_id

    def _team_advance_account(self):
        self.ensure_one()
        if not self.advance_account_id:
            raise ValidationError(_("The CRM Team %s has not advance account") % self.name)
        return self.advance_account_id

    def _compute_kilogram(self):
        if not self:
            return

        query = '''
            SELECT
                move.team_id         AS team_id,
                SUM(line.quantity * product.weight) AS kilogram
            FROM account_move move
            JOIN account_move_line line ON line.move_id = move.id
            JOIN account_account account ON account.id = line.account_id
            JOIN product_product product ON product.id = line.product_id
            WHERE move.move_type IN ('out_invoice', 'out_refund', 'in_invoice', 'in_refund')
            AND move.payment_state IN ('in_payment', 'paid', 'reversed')
            AND move.state = 'posted'
            AND move.team_id IN %s
            AND move.date BETWEEN %s AND %s
            AND line.tax_line_id IS NULL
            AND line.display_type IS NULL
            AND account.internal_type NOT IN ('receivable', 'payable')
            GROUP BY move.team_id
        '''
        today = fields.Date.today()
        params = [tuple(self.ids), fields.Date.to_string(today.replace(day=1)), fields.Date.to_string(today)]
        self._cr.execute(query, params)

        data_map = dict((v[0], v[1]) for v in self._cr.fetchall())
        for team in self:
            team.kilogram = data_map.get(team.id, 0.0)

    def update_kilogram_target(self, value):
        return self.write({'kilogram_target': round(float(value or 0))})
