INSERT INTO delivery_guide (
	id,
	create_date,
	weight,
	write_uid,
	partner_id,
	create_uid,
	state,
	write_date,
	name,
	notes,
	carrier_id,
	price_kg,
	price,
	scheduled_date,
	delivered_date,
	company_id,
	currency_id,
	parent_id
) SELECT
	agofer.id,
	agofer.create_date,
	agofer.weight,
	agofer.write_uid,
	agofer.partner_id,
	agofer.create_uid,
	agofer.state,
	agofer.write_date,
	agofer.name,
	agofer.notes,
	agofer.carrier_id,
	agofer.price_kg,
	agofer.price,
	agofer.scheduled_date,
	agofer.delivered_date,
	--agofer.company_id
	1,
	--agofer.currency_id
	8,
	--agofer.parent_id
	1
FROM dblink('dbname=agofer_08','select
	SPWE.id,
	SPWE.create_date,
	SPWE.weight,
	SPWE.write_uid,
	SPWE.partner_id,
	SPWE.create_uid,
	SPWE.state,
	SPWE.write_date,
	SPWE.name,
	SPWE.note AS notes,
	SPWE.wave_id AS carrier_id,
	SPWE.costo_kilo AS price_kg,
	SPWE.costo_total AS price,
	SPWE.date_schedule AS scheduled_date,
	SPWE.date_deliver AS delivered_date
	from stock_picking_wave_extended SPWE;'
) AS agofer(
	id integer,
	create_date timestamp without time zone,
	weight numeric,
	write_uid integer,
	partner_id integer,
	create_uid integer,
	state character varying,
	write_date timestamp without time zone,
	name character varying,
	notes text,
	carrier_id integer,
	price_kg numeric,
	price numeric,
	scheduled_date date,
	delivered_date date
)
INNER JOIN delivery_carrier DC ON DC.id = agofer.carrier_id;

select setval('delivery_guide_id_seq', (select max(id) from delivery_guide));