INSERT INTO res_country (
	id, 
	code,
	create_date, 
	write_uid, 
	currency_id, 
	write_date, 
	create_uid, 
	name, 
	address_format,
	street_format
) SELECT
    agofer.id,
	agofer.code,
	agofer.create_date,
	--agofer.write_uid
	2, 
	agofer.currency_id, 
	agofer.write_date,
    --agofer.create_uid
	2, 
	agofer.name || '.',
	agofer.address_format,
	--agofer.street_format
	'%(street_number)s/%(street_number2)s %(street_name)s'
FROM dblink('dbname=agofer_08', 'select
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
)AS agofer(
	id integer, 
	code character varying, 
	create_date timestamp without time zone, 
	write_uid integer, 
	currency_id integer, 
	write_date timestamp without time zone, 
	create_uid integer, 
	name character varying, 
	address_format text
)
WHERE agofer.id NOT IN (SELECT id FROM res_country);
