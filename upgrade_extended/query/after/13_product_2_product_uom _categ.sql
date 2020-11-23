insert into uom_category (
	id, 
	create_uid, 
	create_date, 
	name, 
	write_uid, 
	write_date)
	select agofer.id, 
	agofer.create_uid, 
	agofer.create_date, 
	agofer.name, 
	agofer.write_uid, 
	agofer.write_date
from dblink('dbname=agofer_08', 'select 
	id, 
	create_uid, 
	create_date, 
	name, 
	write_uid, 
	write_date
	from product_uom_categ;'
) as agofer(
	id integer, 
	create_uid integer, 
	create_date timestamp without time zone, 
	name character varying, 
	write_uid integer, 
	write_date timestamp without time zone) 
	where agofer.id not in (select id from uom_category);