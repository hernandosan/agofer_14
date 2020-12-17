insert into stock_quant (
	id, 
	create_date, 
	write_uid, 
	package_id, 
	write_date, 
	lot_id, 
	create_uid, 
	location_id, 
	company_id, 
	product_id, 
	in_date, 
	owner_id,
	quantity
) select 
	agofer.id, 
	agofer.create_date, 
	agofer.write_uid, 
	agofer.package_id, 
	agofer.write_date, 
	agofer.lot_id, 
	agofer.create_uid, 
	agofer.location_id, 
	agofer.company_id, 
	agofer.product_id, 
	agofer.in_date, 
	agofer.owner_id,
	agofer.qty
from dblink('dbname=agofer_08','SELECT 
	id, 
	create_date, 
	write_uid, 
	package_id, 
	write_date, 
	lot_id, 
	create_uid, 
	location_id, 
	company_id, 
	product_id, 
	in_date, 
	owner_id,
	qty
	FROM stock_quant;'
) as agofer(
	id integer, 
	create_date timestamp without time zone, 
	write_uid integer, 
	package_id integer, 
	write_date timestamp without time zone, 
	lot_id integer, 
	create_uid integer, 
	location_id integer, 
	company_id integer, 
	product_id integer, 
	in_date timestamp without time zone, 
	owner_id integer,
	qty double precision
);

select setval('stock_quant_id_seq', (select max(id) from stock_quant));

update stock_quant sq 
set location_id = 
case
	when agofer.location_id = 5 then 14 
	when agofer.location_id = 7 then 15 
	else 5 
end
from dblink('dbname=agofer_08','select id, location_id from stock_quant where location_id in (5, 7, 9);') as agofer 
(id integer, location_id integer) 
where agofer.id = sq.id;