INSERT INTO account_payment_order(
	id, 
    create_uid,
    date_prefered,
    date_done,
    company_id,
    write_uid,
    state,
    write_date,
    date_scheduled,
    create_date
) SELECT
	agofer.id, 
    agofer.create_uid,
    agofer.date_prefered,
    agofer.date_done,
    agofer.company_id,
    agofer.write_uid,
    agofer.state,
    agofer.write_date,
    agofer.date_scheduled,
    agofer.create_date
FROM dblink('dbname=agofer_08','select
	id, 
    create_uid,
    date_prefered,
    date_done,
    company_id,
    write_uid,
    state,
    write_date,
    date_scheduled,
    create_date
	from payment_order;'
) AS agofer(
	id integer, 
    create_uid integer,
    date_prefered character varying,
    date_done date,
    company_id integer,
    write_uid integer,
    state character varying,
    write_date timestamp without time zone,
    date_scheduled date,
    create_date timestamp without time zone
);

select setval('account_payment_order_id_seq', (select max(id) from account_payment_order));