insert into stock_valuation_layer (company_id, create_date, product_id, quantity, description)
select 1,
sq.in_date,
sq.product_id, 
sq.quantity,
cast(sq.id as character varying)
from stock_quant sq 
inner join stock_location sl on sl.id = sq.location_id 
where sl.usage = 'internal';

update stock_valuation_layer as svl 
set value = agofer.qty * agofer.cost
from dblink('dbname=agofer_08','select id, qty, cost from stock_quant;') as agofer 
(id integer, qty double precision, cost double precision) 
where cast(svl.description as integer) = agofer.id;