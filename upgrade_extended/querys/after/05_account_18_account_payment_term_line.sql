ALTER TABLE account_payment_term_line DISABLE TRIGGER ALL;
DELETE FROM account_payment_term_line;
ALTER TABLE account_payment_term_line ENABLE TRIGGER ALL;

INSERT INTO account_payment_term_line (
	id,
	payment_id,
	create_uid,
	create_date,
	days,
	value,
	write_uid,
	write_date,
	value_amount,
	option
) SELECT
	agofer.id,
	agofer.payment_id,
	agofer.create_uid,
	agofer.create_date,
	agofer.days,
	agofer.value,
	agofer.write_uid,
	agofer.write_date,
	agofer.value_amount,
	--agofer.option
	'day_after_invoice_date'
FROM dblink('dbname=agofer_08', 'select
	id,
	payment_id,
	create_uid,
	create_date,
	days,
	value,
	write_uid,
	write_date,
	value_amount
    from account_payment_term_line;'
) AS agofer (
	id integer,
	payment_id integer,
	create_uid integer,
	create_date timestamp without time zone,
	days integer,
	value character varying,
	write_uid integer,
	write_date timestamp without time zone,
	value_amount numeric
)
WHERE agofer.id NOT IN (SELECT id FROM account_payment_term_line);

select setval('account_payment_term_line_id_seq', (select max(id) from account_payment_term_line));