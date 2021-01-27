INSERT INTO delivery_guide (
	id,
	create_date,
	write_uid,
	partner_id,
	create_uid,
	state,
	write_date,
	name,
	notes,
	price_kg,
	carrier_id,
	date_scheduled,
	company_id,
	guide_type
) SELECT
	agofer.id,
	agofer.create_date,
	agofer.write_uid,
	agofer.partner_id,
	agofer.create_uid,
	agofer.state,
	agofer.write_date,
	agofer.name,
	agofer.note,
	agofer.costo_kilo,
	agofer.tarifa_id,
	agofer.date_schedule,
	--agofer.company_id
	1,
	'customer'
FROM dblink('dbname=agofer_08','select
	id,
	create_date,
	write_uid,
	partner_id,
	create_uid,
	state,
	write_date,
	name,
	note,
	costo_kilo,
	wave_id,
	date_schedule,
	tarifa_id
	from stock_picking_wave_extended;'
) AS agofer(
	id integer,
	create_date timestamp without time zone,
	write_uid integer,
	partner_id integer,
	create_uid integer,
	state character varying,
	write_date timestamp without time zone,
	name character varying,
	note text,
	costo_kilo numeric,
	wave_id integer,
	date_schedule date,
	tarifa_id integer
);

select setval('delivery_guide_id_seq', (select max(id) from delivery_guide));