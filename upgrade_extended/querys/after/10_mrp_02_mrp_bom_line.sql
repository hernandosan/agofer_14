INSERT INTO mrp_bom_line (
	id,
	create_date,
	sequence,
	write_uid,
	bom_id,
	write_date,
	product_qty,
	create_uid,
	product_id,
	product_uom_id,
	company_id
) SELECT
	agofer.id,
	agofer.create_date,
	agofer.sequence,
	agofer.write_uid,
	agofer.bom_id,
	agofer.write_date,
	agofer.product_qty,
	agofer.create_uid,
	agofer.product_id,
	agofer.product_uom,
	--agofer.company_id
	1
FROM dblink('dbname=agofer_08','select
	id,
	create_date,
	sequence,
	write_uid,
	bom_id,
	write_date,
	product_qty,
	create_uid,
	product_id,
	product_uom
	from mrp_bom_line;'
) AS agofer(
	id integer,
	create_date timestamp without time zone,
	sequence integer,
	write_uid integer,
	bom_id integer,
	write_date timestamp without time zone,
	product_qty numeric,
	create_uid integer,
	product_id integer,
	product_uom integer
);

select setval('mrp_bom_line_id_seq', (select max(id) from mrp_bom_line));