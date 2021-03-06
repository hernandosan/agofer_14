INSERT INTO stock_inventory (
	id, 
	create_uid, 
	create_date, 
	state, 
	company_id, 
	write_uid, 
	write_date, 
	date, 
	name
) SELECT
	agofer.id, 
	agofer.create_uid, 
	agofer.create_date, 
	agofer.state, 
	agofer.company_id, 
	agofer.write_uid, 
	agofer.write_date, 
	agofer.date, 
	agofer.name 
FROM dblink('dbname=agofer_08', 'select
	id, 
	create_uid, 
	create_date, 
	state, 
	company_id, 
	write_uid, 
	write_date, 
	date, 
	name
	from stock_inventory;'
) AS agofer (
	id integer, 
	create_uid integer, 
	create_date timestamp without time zone, 
	state character varying, 
	company_id integer, 
	write_uid integer, 
	write_date timestamp without time zone, 
	date timestamp without time zone, 
	name character varying
);

select setval('stock_inventory_id_seq', (select max(id) from stock_inventory));