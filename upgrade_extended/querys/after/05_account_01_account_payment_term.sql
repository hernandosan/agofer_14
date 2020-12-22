ALTER TABLE account_payment_term DISABLE TRIGGER ALL;
DELETE FROM account_payment_term;
ALTER TABLE account_payment_term ENABLE TRIGGER ALL;

INSERT INTO account_payment_term (
	id,
    create_uid,
    create_date,
    name,
    write_uid,
    note,
    write_date,
    active,
    company_id,
    sequence
) SELECT
	agofer.id,
    agofer.create_uid,
    agofer.create_date,
    agofer.name,
    agofer.write_uid,
    agofer.note,
    agofer.write_date,
    agofer.active,
    --agofer.company_id
    1,
    --agofer.sequence
    10
FROM dblink('dbname=agofer_08','SELECT
	id,
    create_uid,
    create_date,
    name,
    write_uid,
    note,
    write_date,
    active
	FROM account_payment_term;'
) AS agofer(
	id integer,
    create_uid integer,
    create_date timestamp without time zone,
    name character varying,
    write_uid integer,
    note text,
    write_date timestamp without time zone,
    active boolean
);

select setval('account_payment_term_id_seq', (select max(id) from account_payment_term));