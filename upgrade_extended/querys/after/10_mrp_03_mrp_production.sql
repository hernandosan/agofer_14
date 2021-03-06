INSERT INTO mrp_production (
	id,
	origin,
	create_date,
	write_uid,
	product_qty,
	create_uid,
	user_id,
	location_src_id,
	date_start,
	company_id,
	priority,
	state,
	bom_id,
	date_finished,
	write_date,
	name,
	product_id,
	location_dest_id,
	product_uom_id,
	date_planned_start,
	consumption,
	picking_type_id,
	production_type
) SELECT
	agofer.id,
	agofer.origin,
	agofer.create_date,
	agofer.write_uid,
	agofer.product_qty,
	agofer.create_uid,
	agofer.user_id,
	agofer.location_src_id,
	agofer.date_start,
	agofer.company_id,
	agofer.priority,
	agofer.state,
	agofer.bom_id,
	agofer.date_finished,
	agofer.write_date,
	agofer.name,
	agofer.product_id,
	agofer.location_dest_id,
	agofer.product_uom,
	agofer.date_planned,
	--agofer.consumption
	'flexible',
	--agofer.picking_type_id
	617,
	'manufacturing'
FROM dblink('dbname=agofer_08', 'select
	id,
	origin,
	create_date,
	write_uid,
	product_qty,
	create_uid,
	user_id,
	location_src_id,
	date_start,
	company_id,
	priority,
	state,
	bom_id,
	date_finished,
	write_date,
	name,
	product_id,
	location_dest_id,
	product_uom,
	date_planned
	from mrp_production;'
) AS agofer (
	id integer,
	origin character varying,
	create_date timestamp without time zone,
	write_uid integer,
	product_qty numeric,
	create_uid integer,
	user_id integer,
	location_src_id integer,
	date_start timestamp without time zone,
	company_id integer,
	priority character varying,
	state character varying,
	bom_id integer,
	date_finished timestamp without time zone,
	write_date timestamp without time zone,
	name character varying,
	product_id integer,
	location_dest_id integer,
	product_uom integer,
	date_planned timestamp without time zone
);

select setval('mrp_production_id_seq', (select max(id) from mrp_production));

insert into stock_picking_type 
(name, code, sequence_code, create_date, company_id, active)
VALUES ('Production', 'mrp_operation', 'MO', now() at time zone 'UTC', 1, True);

update mrp_production set picking_type_id = (select max(id) from stock_picking_type);