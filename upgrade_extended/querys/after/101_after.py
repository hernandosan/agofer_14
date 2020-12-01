import xmlrpc.client

url = 'http://localhost:8069'
db = 'agofer'
username = 'admin'
password = 'admin'

common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
uid = common.authenticate(db, username, password, {})

# Sentence generation

model = 'stock.quant'
domain = [('quantity', '>=', 0), ('location_id.usage', '=', 'internal')]
ids = models.execute_kw(db, uid, password, model, 'search', [domain])
models.execute_kw(db, uid, password, model, 'write', [ids, {'on_hand': True}])
