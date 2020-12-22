INSERT INTO account_fiscal_position_tax (
	id,
    create_uid,
    create_date,
    position_id,
    tax_src_id,
    write_uid,
    tax_dest_id,
    write_date,
    company_id,
    option
) SELECT
	agofer.id,
    agofer.create_uid,
    agofer.create_date,
    agofer.position_id,
    agofer.tax_src_id,
    agofer.write_uid,
    agofer.tax_dest_id,
    agofer.write_date,
    --agofer.company_id
    1,
    'day_after_invoice_date'
FROM dblink('dbname=agofer_08','select
	id,
    create_uid,
    create_date,
    position_id,
    tax_src_id,
    write_uid,
    tax_dest_id,
    write_date
	from account_fiscal_position_tax;'
) AS agofer(
	id integer,
    create_uid integer,
    create_date timestamp without time zone,
    position_id integer,
    tax_src_id integer,
    write_uid integer,
    tax_dest_id integer,
    write_date timestamp without time zone
);

select setval('account_fiscal_position_id_seq', (select max(id) from account_fiscal_position));