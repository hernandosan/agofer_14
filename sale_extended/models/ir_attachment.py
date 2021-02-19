# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class IrAttachment(models.Model):
    _inherit = 'ir.attachment'

    def unlink(self):
        for attachment in self:
            if (attachment.create_uid != self.env.user) and not self.env.user.has_group('sale_extended.group_delete_attachment'):
                raise UserError(_("You can't delete attachments you didn't create."))
        return super(IrAttachment, self).unlink()
