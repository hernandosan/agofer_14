import base64

from openerp import http


class WebUploadAttachment(http.Controller):
    @http.route('/scan', type='http', auth='user', website=True)
    def website_scan(self):
        error = {}
        return http.request.render("scan_extended.portal_create_scan", {
            'error': error,
        })

    @http.route("/submitted/scan", type="http", auth="user", website=True, csrf=True)
    def submit_scan(self, **kw):
        # Creation of variables
        name = kw.get('prefix_document')
        name2 = kw.get('prefix2_document')
        name3 = kw.get('prefix3_document')
        number = kw.get('number_doc')
        type_document = kw.get('type_document')
        error = ''

        # Data Validation
        if type_document == 'account.move' or type_document == 'sale.order':
            if name.startswith('CF'):
                name = name + '-' + str(number)
            else:
                name = name + str(number)

        if type_document == 'stock.picking':
            number = number.zfill(5)
            name = name + name2 + '/' + name3 + '/' + str(number)

        if type_document == 'delivery.guide':
            number = number.zfill(5)
            name = name + '-' + str(number)

        if type_document == 'account.payment':
            number = number.zfill(6)
            name = name + str(number) + '-' + name2

        if type_document == 'mrp.production':
            if name == 'MO':
                name = name + '/' + number
            elif name == 'PO':
                name = name + number

        # Search in Models
        if type_document != 'selection':
            new_attachment = http.request.env[type_document].sudo().search([("name", "=", name)])

        # Error
        if kw.get('prefix_document') == '--Selection--':
            error = "You have not selected a prefix type for the document"
        elif not new_attachment:
            error = "The document ( " + name + " ) does not exist in the system"

        # Send attachments
        if error == '':
            for c_file in http.request.httprequest.files.getlist("attachment"):
                data = c_file.read()
                if c_file.filename:
                    created = http.request.env["ir.attachment"].sudo().create(
                        {
                            "name": c_file.filename,
                            "datas": base64.b64encode(data),
                            "res_model": type_document,
                            "res_id": new_attachment.id,
                        }
                    )
            return http.request.render("scan_extended.portal_confirm_scan",{
                'name': name,
                'created': str(created.id)
            })
        else:
            return http.request.render("scan_extended.portal_create_scan", {
                'error': error
            })
