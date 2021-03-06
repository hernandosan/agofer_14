INSERT INTO stock_quant (
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
	quantity,
	reserved_quantity
) SELECT
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
	agofer.qty,
	--agofer.reserved_quantity
	0
FROM dblink('dbname=agofer_08','select
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
	from stock_quant;'
) AS agofer(
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