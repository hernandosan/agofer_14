# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class AccountMove(models.Model):
    _inherit = 'account.move'

    import_id = fields.Many2one('purchase.import', 'Import', compute='_compute_import_id', inverse='_set_import_id')
    import_type = fields.Selection([('cif','CIF'),('cost', 'Cost'), ('insurance', 'Insurance'), ('freight','Freight'), 
        ('tariff', 'Tariff'), ('vat','VAT'), ('other', 'Other')], 'Import type', copy=False)
    imports_ids = fields.Many2many('purchase.import', 'import_move_rel', 'move_id', 'import_id', 'Imports', copy=False)
    import_bool = fields.Boolean('Import Bool', copy=False)

    @api.depends('imports_ids')
    def _compute_import_id(self):
        for move in self:
            move.import_id = move.imports_ids[-1] if move.imports_ids else False

    def _set_import_id(self):
        for move in self:
            if move.import_id:
                move.write({'imports_ids': [(6, 0, [move.import_id.id])]})


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    import_type = fields.Selection(related='move_id.import_type', store=True)
