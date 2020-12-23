INSERT INTO purchase_import (
	id, 
	partner_id, 
	origin, 
	date_import, 
	create_date, 
	write_uid, 
	currency_id, 
	company_id, 
	state, 
	create_uid, 
	write_date, 
	currency_rate, 
	name, 
	incoterm_id
) SELECT
	agofer.id, 
	agofer.trading_id, 
	agofer.origin, 
	cast(agofer.create_date as timestamp without time zone), 
	create_date, 
	agofer.write_uid, 
	agofer.currency_id, 
	agofer.company_id, 
	agofer.state, 
	agofer.create_uid, 
	agofer.write_date, 
	agofer.currency_rate, 
	agofer.name,
	agofer.incoterm_id
FROM dblink('dbname=agofer_08', 'select
	id, 
	trading_id, 
	origin, 
	date_origin, 
	create_date, 
	write_uid, 
	currency_id, 
	company_id, 
	state, 
	create_uid, 
	write_date, 
	currency_rate, 
	name, 
	incoterm_id
	from purchase_import;'
) as agofer (
	id integer, 
	trading_id integer, 
	origin integer, 
	date_origin date, 
	create_date timestamp without time zone, 
	write_uid integer, 
	currency_id integer, 
	company_id integer, 
	state character varying, 
	create_uid integer, 
	write_date timestamp without time zone, 
	currency_rate numeric, 
	name character varying, 
	incoterm_id integer
);

select setval('purchase_import_id_seq', (select max(id) from purchase_import));
