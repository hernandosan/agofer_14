insert into product_pricelist (
	id, 
	create_date, 
	write_uid, 
	currency_id, 
	write_date, 
	active, 
	create_uid, 
	name, 
	company_id,
	discount_policy
) select 
	agofer.id, 
	agofer.create_date, 
	agofer.write_uid, 
	--agofer.currency_id,
	8, 
	agofer.write_date, 
	agofer.active, 
	agofer.create_uid, 
	agofer.name, 
	agofer.company_id,
	'with_discount'
from dblink('dbname=agofer_08', 'select 
	id, 
	create_date, 
	write_uid, 
	currency_id, 
	write_date, 
	active, 
	create_uid, 
	name, 
	company_id
	from product_pricelist;'
) as agofer (
	id integer, 
	create_date timestamp without time zone, 
	write_uid integer, 
	currency_id integer, 
	write_date timestamp without time zone, 
	active boolean, 
	create_uid integer, 
	name character varying, 
	company_id integer
) where agofer.id not in (select id from product_pricelist);