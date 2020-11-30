import xmlrpc.client

url = 'http://localhost:8069'
db = 'agofer'
username = 'admin'
password = 'admin'

common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
uid = common.authenticate(db, username, password, {})

ids = models.execute_kw(db, uid, password, 'res.users', 'search', [[]])
models.execute_kw(db, uid, password, 'res.users', 'write', [ids, {'company_ids': [(4,1,0)]}])