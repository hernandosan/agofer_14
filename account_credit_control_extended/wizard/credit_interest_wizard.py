from odoo import fields, models, api, _
from odoo.exceptions import UserError
import base64, num2words


class CreditInterestWizard(models.Model):
    _name = 'credit.interest.wizard'
    _description = 'Credit Interest Wizard'

    partner_id = fields.Many2one('res.partner', 'Partner')
    annual_cash = fields.Float('Annual Cash', required=True, digits=(2, 2))
    month_expired = fields.Float('Month Expired', digits=(2, 2))
    payment_date = fields.Date('Payment Date', default=fields.Date.today())
    lines_ids = fields.Many2many('account.move.line', string='Invoices')
    line_ids = fields.One2many('credit.interest.line.wizard', 'interest_id', 'Lines')
    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env.company)
    currency_id = fields.Many2one(related='company_id.currency_id')
    amount_untaxed = fields.Monetary('Amount Untaxed', compute='_compute_amount')
    amount_taxed = fields.Monetary('Amount Taxed', compute='_compute_amount')
    amount_total = fields.Monetary('Amount Total', compute='_compute_amount')
    attachment_id = fields.Many2one('ir.attachment', 'Attachment')
    file_data = fields.Binary('File')
    file_name = fields.Char('File Name')

    @api.onchange('annual_cash')
    def onchange_annual_cash(self):
        self.month_expired = (pow(1 + (self.annual_cash/100), (1/12))-1)*100

    def return_month_expired(self, annual_cash):
        self.ensure_one()
        month_expired = (pow(1 + annual_cash/100, (1 / 12)) - 1) * 100
        return round(month_expired, 2)

    def _compute_amount(self):
        for record in self:
            amount_untaxed = 0
            amount_taxed = 0
            amount_total = 0
            for line in record.line_ids:
                amount_untaxed += line.amount_untaxed
                amount_taxed += line.amount_taxed
                amount_total += line.amount
            record.amount_untaxed = round(amount_untaxed, 2)
            record.amount_taxed = round(amount_taxed, 2)
            record.amount_total = round(amount_total, 2)

    def action_interest(self):
        this = self[0]
        self.line_ids.unlink()
        line_ids = []
        for line in self.lines_ids:
            vals = {
                'invoice_id': line.move_id.id,
                'line_id': line.id
            }
            line_ids.append((0, 0, vals))
        self.write({
            'line_ids': line_ids,
        })
        file_name, file_data = self._create_attachment()
        self.write({
            'file_name': file_name,
            'file_data': file_data
        })
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'credit.interest.wizard',
            'view_mode': 'form',
            'res_id': this.id,
            'views': [(False, 'form')],
            'target': 'new',
        }

    def _create_attachment(self):
        self.ensure_one()
        report_name = self.partner_id.name
        report = self.env.ref('account_credit_control_extended.report_credit_interest_wizard')
        res_id = self.id
        report_service = report.report_name

        if report.report_type in ['qweb-html', 'qweb-pdf']:
            result, format = report._render_qweb_pdf([res_id])
        else:
            res = report._render([res_id])
            if not res:
                raise UserError(_('Unsupported report type %s found.', report.report_type))
            result, format = res

        result = base64.b64encode(result)
        if not report_name:
            report_name = 'report.' + report_service
        ext = "." + format
        if not report_name.endswith(ext):
            report_name += ext

        return report_name, result

    def num2word(self):
        self.ensure_one()
        return num2words.num2words(self.amount_total, lang=self.partner_id.lang)


class CreditInterestLineWizard(models.Model):
    _name = 'credit.interest.line.wizard'
    _description = 'Credit Interest Line Wizard'

    interest_id = fields.Many2one('credit.interest.wizard', 'Interest', ondelete='cascade')
    annual_cash = fields.Float(related='interest_id.annual_cash')
    payment_date = fields.Date(related='interest_id.payment_date')
    days_maturity = fields.Integer('Days of Arrears', compute='_compute_days_maturity')
    invoice_id = fields.Many2one('account.move', 'Invoice')
    invoice_date = fields.Date(related='invoice_id.invoice_date')
    line_id = fields.Many2one('account.move.line', 'Line')
    date_maturity = fields.Date(related='line_id.date_maturity')
    invoice_payment_term_id = fields.Many2one(related='invoice_id.invoice_payment_term_id')
    currency_id = fields.Many2one(related='invoice_id.company_currency_id')
    amount_total = fields.Monetary(related='invoice_id.amount_total')
    amount_residual = fields.Monetary(related='invoice_id.amount_residual')
    amount_untaxed = fields.Monetary('Amount Untaxed', compute='_compute_amount')
    amount_taxed = fields.Monetary('Amount Taxed', compute='_compute_amount')
    amount = fields.Monetary('Amount Total', compute='_compute_amount')

    @api.depends('payment_date', 'date_maturity')
    def _compute_days_maturity(self):
        for record in self:
            if record.payment_date and record.date_maturity:
                record.days_maturity = (fields.Date.from_string(record.payment_date)
                                        - fields.Date.from_string(record.date_maturity)).days
            else:
                record.days_maturity = 0

    def _compute_amount(self):
        for record in self:
            amount_untaxed = (record.amount_residual * record.days_maturity * (record.annual_cash/100))/360
            amount_taxed = amount_untaxed * 0.19
            amount_total = amount_untaxed + amount_taxed
            record.amount_untaxed = amount_untaxed
            record.amount_taxed = amount_taxed
            record.amount = amount_total
