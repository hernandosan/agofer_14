insert into delivery_carrier (
	id, 
	create_uid, 
	create_date, 
	product_id, 
	write_uid, 
	amount, 
	write_date, 
	active, 
	partner_id, 
	name,
	invoice_policy,
	delivery_type
) select 
	agofer.id, 
	agofer.create_uid, 
	agofer.create_date, 
	agofer.product_id, 
	agofer.write_uid, 
	agofer.amount, 
	agofer.write_date, 
	agofer.active, 
	agofer.partner_id, 
	agofer.name,
	'estimated',
	'fixed'
from dblink('dbname=agofer_08','select 
	id, 
	create_uid, 
	create_date, 
	product_id, 
	write_uid, 
	amount, 
	write_date, 
	active, 
	partner_id, 
	name
	from delivery_carrier;'
) as agofer(
	id integer, 
	create_uid integer, 
	create_date timestamp without time zone, 
	product_id integer, 
	write_uid integer, 
	amount double precision, 
	write_date timestamp without time zone, 
	active boolean, 
	partner_id integer, 
	name character varying
) where agofer.id not in (select id from delivery_carrier);