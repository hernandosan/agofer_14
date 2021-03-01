INSERT INTO account_payment (
   id,
    create_date,
    partner_id,
    create_uid,
    write_date,
    write_uid,
    move_id,
    amount
) SELECT
    agofer.id,
    agofer.create_date,
    agofer.partner_id,
    agofer.create_uid,
    agofer.write_date,
    agofer.write_uid,
    agofer.move_id,
    agofer.amount
FROM dblink('dbname=agofer_08', 'select
        id,
        create_date,
        partner_id,
        create_uid,
        write_date,
        write_uid,
        move_id,
        amount
        from account_voucher;'
) AS agofer(
    id integer,
    create_date timestamp without time zone,
    partner_id integer,
    create_uid integer,
    write_date timestamp without time zone,
    write_uid integer,
    move_id integer,
    amount numeric
);

SELECT setval('account_payment_id_seq', (SELECT max(id) FROM account_payment));