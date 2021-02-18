-- ALTER TABLE account_journal DISABLE TRIGGER ALL;
-- DELETE FROM account_journal;
-- ALTER TABLE account_journal ENABLE TRIGGER ALL;

UPDATE account_journal AS aj 
SET code = agofer.code, 
	create_date = agofer.create_date, 
	write_uid = agofer.write_uid, 
	loss_account_id = agofer.loss_account_id, 
	write_date = agofer.write_date, 
	create_uid = agofer.create_uid, 
	name = agofer.name, 
	company_id = agofer.company_id, 
	profit_account_id = agofer.profit_account_id, 
	type = agofer.type,
	sequence_id = agofer.sequence_id,
	currency_id = agofer.currency 
FROM dblink('dbname=agofer_08','select
	id, 
	code, 
	create_date, 
	write_uid, 
	loss_account_id, 
	write_date, 
	create_uid, 
	name, 
	company_id, 
	profit_account_id, 
	type,
	sequence_id,
	currency
	from account_journal;'
) AS agofer(
	id integer, 
	code character varying, 
	create_date timestamp without time zone, 
	write_uid integer, 
	loss_account_id integer, 
	write_date timestamp without time zone, 
	create_uid integer, 
	name character varying, 
	company_id integer, 
	profit_account_id integer, 
	type character varying,
	sequence_id integer,
	currency integer
)
WHERE aj.id = agofer.id;

INSERT INTO account_journal (
	id, 
	code, 
	create_date, 
	write_uid, 
	loss_account_id, 
	write_date, 
	create_uid, 
	name, 
	company_id, 
	profit_account_id, 
	type,
	sequence,
	currency_id,
	invoice_reference_type,
	invoice_reference_model,
	active
) SELECT
	agofer.id, 
	agofer.code, 
	agofer.create_date, 
	agofer.write_uid, 
	agofer.loss_account_id, 
	agofer.write_date, 
	agofer.create_uid, 
	agofer.name, 
	agofer.company_id, 
	agofer.profit_account_id, 
	agofer.type,
	agofer.sequence_id,
	agofer.currency,
	--agofer.invoice_reference_type
	'invoice',
	--agofer.invoice_reference_model
	'odoo',
	--agofer.active
	True
FROM dblink('dbname=agofer_08','select
	id, 
	code, 
	create_date, 
	write_uid, 
	loss_account_id, 
	write_date, 
	create_uid, 
	name, 
	company_id, 
	profit_account_id, 
	type,
	sequence_id,
	currency
	from account_journal;'
) AS agofer(
	id integer, 
	code character varying, 
	create_date timestamp without time zone, 
	write_uid integer, 
	loss_account_id integer, 
	write_date timestamp without time zone, 
	create_uid integer, 
	name character varying, 
	company_id integer, 
	profit_account_id integer, 
	type character varying,
	sequence_id integer,
	currency integer
) WHERE agofer.id not in (SELECT id from account_journal);

select setval('account_journal_id_seq', (select max(id) from account_journal));