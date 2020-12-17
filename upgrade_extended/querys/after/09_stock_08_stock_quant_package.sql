INSERT INTO stock_quant_package (
	id, 
	create_uid, 
	create_date, 
	name, 
	company_id, 
	write_uid, 
	write_date, 
	packaging_id, 
	location_id
) SELECT
	agofer.id, 
	agofer.create_uid, 
	agofer.create_date, 
	agofer.name, 
	agofer.company_id, 
	agofer.write_uid, 
	agofer.write_date, 
	agofer.packaging_id, 
	agofer.location_id
FROM dblink('dbname=agofer_08','SELECT
	id, 
	create_uid, 
	create_date, 
	name, 
	company_id, 
	write_uid, 
	write_date, 
	packaging_id, 
	location_id
	FROM stock_quant_package;'
) AS agofer(
	id integer, 
	create_uid integer, 
	create_date timestamp without time zone, 
	name character varying, 
	company_id integer, 
	write_uid integer, 
	write_date timestamp without time zone, 
	packaging_id integer, 
	location_id integer
);

select setval('stock_quant_package_id_seq', (select max(id) from stock_quant_package));