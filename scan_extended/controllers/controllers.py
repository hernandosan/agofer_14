import base64

from openerp import http
from datetime import datetime
import pytz


class WebUploadAttachment(http.Controller):
    @http.route('/scan', type='http', auth='user', website=True)
    def website_scan(self):
        return http.request.render("scan_extended.portal_create_scan")

    @http.route("/submitted/scan", type="http", auth="user", website=True, csrf=True)
    def submit_scan(self, **post):
        ident = {
            'account.move': 'number',
            'account.voucher': 'number',
            'sale.order': 'name',
            'stock.picking': 'name',
            'stock.picking.wave.extended': 'name',
            'mrp.production': 'name',
            'production.extended': 'name',
        }

        type_document = post.get('type_document')

        # error = {}
        # prefixes = ''.join([str(post.get(k)) for k in sorted(post) if k.startswith('prefix')])
        # suffixes = ''.join([str(post.get(k)) for k in sorted(post) if k.startswith('suffix')])
        # if prefixes.startswith('IE'):
        #     prefixes = prefixes.replace('-', '')
        # if prefixes.startswith('PO'):
        #     prefixes = prefixes.replace('/', '')
        #
        # if not post.get('attachment'):
        #     error['attachment'] = 'missing'
        # filefield = post.get('attachment')
        # if post.get("attachment"):
        #     for c_file in http.request.httprequest.files.getlist("attachment"):
        #         data = c_file.read()
        #         if c_file.filename:
        #             http.request.env["ir.attachment"].sudo().create(
        #                 {
        #                     "name": c_file.filename,
        #                     "datas": base64.b64encode(data),
        #                 }
        #             )
        #
        # numero = post.get('numero')
        # if not (numero and numero.isdigit()):
        #     error['numero'] = 'No se encuentra ese documento.'
        #
        # type_document = post.get('type_document')
        # if (type_document not in ident):
        #     error['numero'] = 'No se encuentra el tipo de documento.'
        # else:
        #     if numero not in error and type_document == 'stock.picking.wave.extended':
        #         numero = numero.zfill(5)
        #     elif numero not in error and type_document == 'account.voucher':
        #         numero = numero.zfill(6)
        #     elif numero not in error and prefixes.startswith('MO'):
        #         numero = numero.zfill(5)
        #     elif numero not in error and prefixes.startswith('PO'):
        #         type_document = 'production.extended'
        #     doc = http.request.env[type_document].search([(ident[type_document], '=', prefixes + numero + suffixes)])
        #     if not doc:
        #         error['attachment'] = 'No se encuentra el documento %s.' % doc
        #
        # created = False
        # try:
        #     tz = pytz.timezone(http.request.env.user.tz) or pytz.utc
        #     hour = datetime.now(tz).strftime("%Y-%m-%d_%H:%M:%S")
        #     msg = ''
        #     for fileitem in filefield:
        #         created = http.request.env['ir.attachment'].create({
        #             'type': 'binary',
        #             'res_model': type_document,
        #             'res_id': doc.id,
        #             'name': fileitem.filename,
        #             'description': 'GO_' + hour,
        #             'datas_fname': fileitem.filename,
        #             'datas': base64.encodestring(fileitem.read()),
        #         })
        #         msg += created and str(created.id) + ', ' or ''
        # except Exception as e:
        #     error['attachment'] = "creating: %s" % str(e) or repr(e)
        #
        # if error:
        #     """
        #     request.session['web_upload_attachments_error'] = error
        #     request.session['web_upload_attachments_default'] = post
        #     """
        #     return http.request.render("scan_extended.portal_create_scan", {
        #         'error': error,
        #         'default': post,
        #     })
        #
        # return http.request.render("web_upload_attachments.gracias", {
        #     'created': msg or 'Error',
        #     'doc': '{} (#{})'.format(doc[ident[type_document]], str(doc.id)),
        # })
