ALTER TABLE delivery_carrier DISABLE TRIGGER ALL;
DELETE FROM delivery_carrier;
ALTER TABLE delivery_carrier ENABLE TRIGGER ALL;

INSERT INTO delivery_carrier (
	id,
	tolerance,
	create_uid,
	create_date,
	name,
	write_uid,
	notes,
	write_date,
	partner_id,
	product_id,
	active,
	invoice_policy,
	delivery_type,
	zip_from,
	zip_to,
	company_id,
	carrier_type
) SELECT
	agofer.id,
	agofer.tolerance,
	agofer.create_uid,
	agofer.create_date,
	agofer.name,
	agofer.write_uid,
	agofer.notes,
	agofer.write_date,
	agofer.partner_id,
	agofer.product_id,
	--agofer.active
	TRUE,
	--agofer.invoice_policy
	'estimated',
	--agofer.delivery_type
	'fixed',
	agofer.zip_from,
	agofer.zip_to,
	--agofer.company_id
	1,
	--agofer.carrier_type
	'stock'
FROM dblink('dbname=agofer_08','select
	SPWT.id,
	SPWT.tolerancia AS tolerance,
	SPWT.create_uid,
	SPWT.create_date,
	SPWT.name,
	SPWT.write_uid,
	SPWT.note AS notes,
	SPWT.write_date,
	SPWT.partner_id,
	SPWT.product_id,
	SPWT.origen AS zip_from,
	SPWT.destino AS zip_to
	from stock_picking_wave_tarifa SPWT;'
) AS agofer(
	id integer,
	tolerance double precision,
	create_uid integer,
	create_date timestamp without time zone,
	name character varying,
	write_uid integer,
	notes text,
	write_date timestamp without time zone,
	partner_id integer,
	product_id integer,
	zip_from character varying,
	zip_to character varying
);

select setval('delivery_carrier_id_seq', (select max(id) from delivery_carrier));