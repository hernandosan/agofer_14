# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = 'account.move'

    niif_bool = fields.Selection([('both','Both'),('local','Local'),('niif','NIIF')], 'Local / NIIF', default='both', copy=False)

    def action_post(self):
        res = super(AccountMove, self).action_post()
        for move in self:
            ids = self.line_ids.ids
            sums = sum(line.niif_debit - line.niif_credit for line in self.line_ids)
            if round(sums, move.company_id.currency_id.decimal_places) != 0.0:
                raise UserError(
                    _("Cannot create unbalanced journal entry. Ids: %s\nDifferences NIIF debit - NIIF credit: %s") % (
                    ids, sums))
        return res


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    _sql_constraints = [(
        'check_niif_debit_credit',
        'CHECK(niif_debit + niif_credit >= 0 AND niif_debit * niif_credit = 0)',
        _('Wrong NIIF debit or credit value in accounting entry !')
    )]

    niif_bool = fields.Selection(related='move_id.niif_bool')
<<<<<<< HEAD
    niif_debit = fields.Monetary('NIIF Debit', compute='_compute_niff_debit_credit', currency_field='company_currency_id')
    niif_credit = fields.Monetary(string='NIIF Credit', compute='_compute_niff_debit_credit', currency_field='company_currency_id')
    niif_balance = fields.Monetary(string='NIIF Balance', currency_field='company_currency_id', compute='_compute_niif_balance')
=======
    niif_debit = fields.Monetary('NIIF Debit', default=0.0, currency_field='company_currency_id')
    niif_credit = fields.Monetary(string='NIIF Credit', default=0.0, currency_field='company_currency_id')
    niif_balance = fields.Monetary(string='NIIF Balance', currency_field='company_currency_id',
                                   compute='_compute_niif_balance')
>>>>>>> 06d071e7b6eed5eff6dca7aa922f3c67cff210c9

    @api.depends('niif_bool', 'debit', 'credit')
    def _compute_niff_debit_credit(self):
        for line in self:
            vals = {}
            if niif_bool == 'both':
                vals.update(niif_debit=line.debit, niif_credit=line.credit)
            if niif_bool == 'local':
                vals.update(niif_debit=0.0, niif_credit=0.0)
            line.update(vals)

    def _inverse_niff_debit_credit(self):
        for line in self:
            vals = {}
            if niif_bool == 'niif':
                vals.update(debit=line.niif_debit, credit=line.niif_credit)
            line.update(vals)

    @api.depends('niif_debit', 'niif_credit')
    def _compute_niif_balance(self):
        for line in self:
            line.niif_balance = line.niif_debit - line.niif_credit

    @api.model_create_multi
    def create(self, vals_list):
        lines = super(AccountMoveLine, self).create(vals_list)
        lines.prepare_values_write(vals_list, list=True)
        return lines
<<<<<<< HEAD
=======

    def write(self, vals):
        res = super(AccountMoveLine, self).write(vals)
        self.prepare_values_write(vals)
        return res

    def prepare_values_write(self, vals, list=False):
        for i, line in enumerate(self):
            values = vals[i] if list else vals
            line._prepare_values_write(values)

    def _prepare_values_write(self, vals):
        self.ensure_one()
        if 'debit' in vals or 'credit' in vals:
            for line in self:
                niif_bool = line.niif_bool
                values = {}
                if niif_bool == 'both':
                    values.update(niif_debit=vals.get('debit') or line.debit,
                                  niif_credit=vals.get('credit') or line.credit)
                elif niif_bool == 'local':
                    values.update(niif_debit=0.0, niif_credit=0.0)
                else:
                    continue
                    # vals.update(debit=0.0, credit=0.0)
                line.write(values)
>>>>>>> 06d071e7b6eed5eff6dca7aa922f3c67cff210c9
