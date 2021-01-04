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
	carrier_type,
	price_kg
) SELECT
	agofer.id,
	agofer.tolerancia,
	agofer.create_uid,
	agofer.create_date,
	agofer.name,
	agofer.write_uid,
	agofer.note,
	agofer.write_date,
	agofer.partner_id,
	agofer.product_id,
	--agofer.active
	TRUE,
	--agofer.invoice_policy
	'estimated',
	--agofer.delivery_type
	'fixed',
	agofer.origen,
	agofer.destino,
	--agofer.company_id
	1,
	--agofer.carrier_type
	'stock',
	--agofer.price_kg
	cast(agofer.valor as double precision)
FROM dblink('dbname=agofer_08','select
	id,
	tolerancia,
	create_uid,
	create_date,
	name,
	write_uid,
	note,
	write_date,
	partner_id,
	product_id,
	origen,
    destino,
	valor
	from stock_picking_wave_tarifa;'
) AS agofer(
	id integer,
	tolerancia double precision,
	create_uid integer,
	create_date timestamp without time zone,
	name character varying,
	write_uid integer,
	note text,
	write_date timestamp without time zone,
	partner_id integer,
	product_id integer,
	origen character varying,
	destino character varying,
	valor numeric
);

select setval('delivery_carrier_id_seq', (select max(id) from delivery_carrier));