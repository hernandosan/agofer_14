# -*- coding: utf-8 -*-

from odoo import models, fields


class AccountConsignmentWizard(models.TransientModel):
    _name = 'account.consignment.wizard'
    _description = 'Account Consignment Wizard'

    consignments_ids = fields.Many2many('account.consignment' 'Consignments', 
        default=lambda self: self.env['account.consignment'].browse(self._context.get('active_id')))
    
    def action_confirm(self):
        self.consignments_ids.action_done()
