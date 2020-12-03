import xmlrpc.client

url = 'http://localhost:8014/'
db = 'agofer_14'
username = 'reyes@reyes'
password = 'hernando'
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))


ids = models.execute_kw(db, uid, password, 'res.users', 'search', [[]])
models.execute_kw(db, uid, password, 'res.users', 'write', [ids, {'company_ids': [(4,1,0)]}])
