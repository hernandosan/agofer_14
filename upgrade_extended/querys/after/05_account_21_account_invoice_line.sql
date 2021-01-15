update account_move_line as aml 
set exclude_from_invoice_tab = False, 
price_unit = agofer.price_unit,
price_subtotal = agofer.price_subtotal 
from dblink('dbname=agofer_08','select aml.id, ail.price_unit, ail.price_subtotal
from account_invoice_line ail 
inner join account_invoice ai on ai.id = ail.invoice_id 
inner join account_move_line aml on aml.move_id = ai.move_id 
where ail.product_id = aml.product_id') as agofer 
(id integer, price_unit numeric, price_subtotal numeric) 
where aml.id = agofer.id;