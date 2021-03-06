INSERT INTO account_payment_mode(
	id, 
    create_uid,
    create_date,
    name,
    company_id,
    write_date,
    write_uid,
	bank_account_link,
	payment_method_id
) SELECT
	agofer.id,
    agofer.create_uid,
    agofer.create_date,
    agofer.name,
    agofer.company_id,
    agofer.write_date,
    agofer.write_uid,
	--agofer.bank_account_link
	'fixed',
	--agofer.payment_method_id
	1
FROM dblink('dbname=agofer_08','select
	id,
    create_uid,
    create_date,
    name,
    company_id,
    write_date,
    write_uid
	from payment_mode;'
) AS agofer(
	id integer,
    create_uid integer,
    create_date timestamp without time zone,
    name character varying,
    company_id integer,
    write_date timestamp without time zone,
    write_uid integer
);

select setval('account_payment_mode_id_seq', (select max(id) from account_payment_mode));