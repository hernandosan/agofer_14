INSERT INTO sale_order_line (
	id,
	create_date,
	product_uom,
	sequence,
	order_id,
	price_unit,
	product_uom_qty,
	write_uid,
	discount,
	write_date,
	salesman_id,
	create_uid,
	product_id,
	company_id,
	name,
	state,
	order_partner_id,
	route_id,
	product_packaging,
	is_delivery,
	upload_delay,
	customer_lead,
	display_type
) SELECT
	agofer.id,
	agofer.create_date,
	agofer.product_uom,
	agofer.sequence,
	agofer.order_id,
	agofer.price_unit,
	agofer.product_uom_qty,
	agofer.write_uid,
	agofer.discount,
	agofer.write_date,
	agofer.salesman_id,
	agofer.create_uid,
	agofer.product_id,
	agofer.company_id,
	agofer.name,
	--agofer.state,
    (CASE WHEN agofer.state = 'confirmed' THEN 'sale' ELSE agofer.state END),
	agofer.order_partner_id,
	agofer.route_id,
	agofer.product_packaging,
	agofer.is_delivery,
	agofer.upload_delay,
	agofer.delay,
	--agofer.display_type
	null
FROM dblink('dbname=agofer_08','select
	id,
	create_date,
	product_uom,
	sequence,
	order_id,
	price_unit,
	product_uom_qty,
	write_uid,
	discount,
	write_date,
	salesman_id,
	create_uid,
	product_id,
	company_id,
	name,
	state,
	order_partner_id,
	route_id,
	product_packaging,
	is_delivery,
	upload_delay,
	delay
	FROM sale_order_line
	WHERE product_id IS NOT null;'
) AS agofer(
	id integer,
	create_date timestamp without time zone,
	product_uom integer,
	sequence integer,
	order_id integer,
	price_unit numeric,
	product_uom_qty numeric,
	write_uid integer,
	discount numeric,
	write_date timestamp without time zone,
	salesman_id integer,
	create_uid integer,
	product_id integer,
	company_id integer,
	name text,
	state character varying,
	order_partner_id integer,
	route_id integer,
	product_packaging integer,
	is_delivery boolean,
	upload_delay double precision,
	delay double precision
);

select setval('sale_order_line_id_seq', (select max(id) from sale_order_line));