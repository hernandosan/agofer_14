insert into res_country (
	id, 
	--code, 
	create_date, 
	write_uid, 
	currency_id, 
	write_date, 
	create_uid, 
	name, 
	--address_format,
	street_format
)select agofer.id, 
	--agofer.code, 
	agofer.create_date, 
	2, 
	agofer.currency_id, 
	agofer.write_date, 
	2, 
	agofer.name || '.', 
	--'%(street)s',
	agofer.address_format
from dblink('dbname=agofer_08', 'select 
	id, 
	code, 
	create_date, 
	write_uid, 
	currency_id, 
	write_date, 
	create_uid, 
	name, 
	address_format
	from res_country;'
)as agofer(
	id integer, 
	code character varying, 
	create_date timestamp without time zone, 
	write_uid integer, 
	currency_id integer, 
	write_date timestamp without time zone, 
	create_uid integer, 
	name character varying, 
	address_format text
)where agofer.id not in (select id from res_country);
