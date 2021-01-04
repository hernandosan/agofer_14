ALTER TABLE account_incoterms DISABLE TRIGGER ALL;
DELETE FROM account_incoterms;
ALTER TABLE account_incoterms ENABLE TRIGGER ALL;

INSERT INTO account_incoterms (
	id,
    create_uid,
    code,
    create_date,
    name,
    write_uid,
    write_date,
    active
) SELECT
	agofer.id,
    agofer.create_uid,
    agofer.code,
    agofer.create_date,
    agofer.name,
    agofer.write_uid,
    agofer.write_date,
    agofer.active
FROM dblink('dbname=agofer_08', 'select
	id,
    create_uid,
    code,
    create_date,
    name,
    write_uid,
    write_date,
    active
    from stock_incoterms;'
) AS agofer (
	id integer,
    create_uid integer,
    code character varying,
    create_date timestamp without time zone,
    name character varying,
    write_uid integer,
    write_date timestamp without time zone,
    active boolean
);

select setval('account_incoterms_id_seq', (select max(id) from account_incoterms));