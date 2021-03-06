INSERT INTO mrp_bom (
	id, 
	code, 
	create_date, 
	sequence, 
	write_uid, 
	write_date, 
	product_qty, 
	active, 
	create_uid, 
	company_id, 
	product_tmpl_id, 
	product_id, 
	type,
	product_uom_id,
	ready_to_produce,
	consumption
) SELECT
	agofer.id, 
	agofer.code, 
	agofer.create_date, 
	agofer.sequence, 
	agofer.write_uid, 
	agofer.write_date, 
	agofer.product_qty, 
	agofer.active, 
	agofer.create_uid, 
	agofer.company_id, 
	agofer.product_tmpl_id, 
	agofer.product_id, 
	agofer.type,
	agofer.product_uom,
	--agofer.ready_to_produce
	'asap',
	--agofer.consumption
	'warning'
FROM dblink('dbname=agofer_08', 'select
	id,
	code,
	create_date,
	sequence,
	write_uid,
	write_date,
	product_qty,
	active,
	create_uid,
	company_id,
	product_tmpl_id,
	product_id,
	type,
	product_uom
	from mrp_bom;'
) AS agofer (
	id integer,
	code character varying,
	create_date timestamp without time zone,
	sequence integer,
	write_uid integer,
	write_date timestamp without time zone,
	product_qty numeric,
	active boolean,
	create_uid integer,
	company_id integer,
	product_tmpl_id integer,
	product_id integer,
	type character varying,
	product_uom integer
);

select setval('mrp_bom_id_seq', (select max(id) from mrp_bom));