import xmlrpc.client

url = 'http://localhost:8014/'
db = 'agofer_14'
username = 'reyes@reyes'
password = 'hernando'
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))


# Sentence generation

model = 'stock.quant'
domain = [('quantity', '>=', 0), ('location_id.usage', '=', 'internal')]
ids = models.execute_kw(db, uid, password, model, 'search', [domain])
models.execute_kw(db, uid, password, model, 'write', [ids, {'on_hand': True}])
