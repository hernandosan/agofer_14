INSERT INTO delivery_guide (
	id,
    create_uid,
    create_date,
    journal_id,
    write_uid,
    state,
    write_date,
    partner_id,
    notes,
    company_id
) SELECT
	agofer.id,
    agofer.create_uid,
    agofer.create_date,
    agofer.journal_id,
    agofer.write_uid,
    agofer.state,
    agofer.write_date,
    agofer.partner_id,
    agofer.note,
    --agofer.company_id
    1
FROM dblink('dbname=agofer_08','select
	id,
    create_uid,
    create_date,
    journal_id,
    write_uid,
    state,
    write_date,
    partner_id,
    note
    from stock_picking_wave_invoice;'
) AS agofer(
	id integer,
    create_uid integer,
    create_date timestamp without time zone,
    journal_id integer,
    write_uid integer,
    state character varying,
    write_date timestamp without time zone,
    partner_id integer,
    note text
);

select setval('delivery_invoice_id_seq', (select max(id) from delivery_invoice));