insert into uom_uom (
	id, 
	create_date, 
	write_uid, 
	active, 
	write_date, 
	uom_type, 
	create_uid, 
	name, 
	rounding, 
	factor, 
	category_id
) select 
	agofer.id, 
	agofer.create_date, 
	agofer.write_uid, 
	agofer.active, 
	agofer.write_date, 
	agofer.uom_type, 
	agofer.create_uid, 
	agofer.name, 
	agofer.rounding, 
	agofer.factor, 
	agofer.category_id
from dblink('dbname=agofer_08', 'select 
	id, 
	create_date, 
	write_uid, 
	active, 
	write_date, 
	uom_type, 
	create_uid, 
	name, 
	rounding, 
	factor, 
	category_id
	from product_uom;'
) as agofer (
	id integer, 
	create_date timestamp without time zone, 
	write_uid integer, 
	active boolean, 
	write_date timestamp without time zone, 
	uom_type character varying, 
	create_uid integer, 
	name character varying, 
	rounding numeric, 
	factor numeric, 
	category_id integer
) where agofer.id not in (select id from uom_uom);

select setval('uom_uom_id_seq', (select max(id) from uom_uom));