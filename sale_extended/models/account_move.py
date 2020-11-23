# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class AccountMove(models.Model):
    _inherit = 'account.move'

    def action_post(self):
        res = super(AccountMove, self).action_post()
        self.action_after_post()
        return res

    def action_after_post(self):
        for move in self.filtered(lambda m: m.move_type == 'out_invoice'):
            move._action_account_corssover()

    def _action_account_corssover(self):
        # Create crossover
        self.ensure_one()
        sale_id = self.sale_id
        if not sale_id:
            return False
        move_vals = self._prepare_crossover_move_values()
        if not move_vals:
            return False
        move_id = self.env['account.move'].create(move_vals)
        move_id.action_post()
        for line in move_id.line_ids:
            line_one = line
            line_two = self.env['account.move.line'].browse(int(line.ref))
            lines = line_one + line_two
            lines.reconcile()
        return True

    def _prepare_crossover_move_values(self):
        self.ensure_one()
        sale_id = self.sale_id
        if not sale_id:
            raise ValidationError(_("The payment %s has not sale order") % self.name)
        journal_id = sale_id.team_id._team_crossover_journal() if sale_id.team_id else sale_id.partner_id._partner_crossover_journal()
        line_ids = self._prepare_crossover_move_line_values()
        if not line_ids:
            return False
        vals = {
            'move_type': 'entry',
            'ref': _('Crossover invoice %s') % self.name,
            'journal_id': journal_id.id,
            'currency_id': self.currency_id.id,
            'line_ids': line_ids
        }
        return vals

    def _prepare_crossover_move_line_values(self):
        self.ensure_one()
        line_ids = []
        reconciled_pays = self.sale_id._sale_payments_id().move_id.line_ids.filtered(lambda line: line.account_id.user_type_id.type in ('receivable', 'payable'))
        amount_pay = abs(sum(line.currency_id.with_context(date=line.date).compute(line.amount_residual, self.currency_id) for line in reconciled_pays)) or 0.0
        reconciled_lines = self.line_ids.filtered(lambda line: line.account_id.user_type_id.type in ('receivable', 'payable'))
        amount_line = abs(sum(line.currency_id.with_context(date=line.date).compute(line.amount_residual, self.currency_id) for line in reconciled_lines)) or 0.0
        if not amount_pay or not amount_line:
            return False
        for invoice in self._prepare_crossover_move_line_invoice_values(reconciled_pays, amount_pay, reconciled_lines, amount_line):
            line_ids.append((0,0,invoice))
        for pay in self._prepare_crossover_move_line_pay_values(reconciled_pays, amount_pay, reconciled_lines, amount_line):
            line_ids.append((0,0,pay))
        return line_ids

    def _prepare_crossover_move_line_pay_values(self, pays, amount_pay, lines, amount_line):
        self.ensure_one()
        vals = []
        amount_payed = 0
        for pay in pays:
            if amount_payed >= amount_line:
                break
            currency_id = self.currency_id
            amount = abs(pay.currency_id.with_context(date=pay.date).compute(pay.amount_residual, currency_id))
            amount = amount if amount + amount_payed <= amount_line else amount_line - amount_payed
            amount_payed += amount
            val = {
                'account_id': pay.account_id.id,
                'partner_id': pay.partner_id.id,
                'name': pay.move_id.name,
                'currency_id': currency_id.id,
                'debit': amount if pay.balance < 0.0 else 0.0,
                'credit': amount if pay.balance > 0.0 else 0.0,
                'ref': str(pay.id)
            }
            vals.append(val)
        return vals

    def _prepare_crossover_move_line_invoice_values(self, pays, amount_pay, lines, amount_line):
        self.ensure_one()
        vals = []
        amount_lined = 0
        for line in lines:
            if amount_lined >= amount_pay:
                break
            currency_id = self.currency_id
            amount = abs(line.currency_id.with_context(date=line.date).compute(line.amount_residual, currency_id))
            amount = amount if amount + amount_lined <= amount_pay else amount_pay - amount_lined
            amount_lined += amount
            val = {
                'account_id': line.account_id.id,
                'partner_id': line.partner_id.id,
                'name': line.move_id.name,
                'currency_id': currency_id.id,
                'debit': amount if line.balance < 0.0 else 0.0,
                'credit': amount if line.balance > 0.0 else 0.0,
                'ref': str(line.id)
            }
            vals.append(val)
        return vals
