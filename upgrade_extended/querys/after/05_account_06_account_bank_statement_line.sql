INSERT INTO account_bank_statement_line (
	id, 
	statement_id, 
	sequence, 
	currency_id, 
	write_date, 
	create_date, 
	write_uid, 
	partner_id, 
	create_uid, 
	partner_name, 
	amount, 
	amount_currency,
	move_id,
	payment_ref
) SELECT
	agofer.id, 
	--agofer.statement_id,
	(CASE WHEN agofer.statement_id IS null THEN 350 ELSE agofer.statement_id END),
	agofer.sequence, 
	agofer.currency_id, 
	agofer.write_date, 
	agofer.create_date, 
	agofer.write_uid, 
	agofer.partner_id, 
	agofer.create_uid, 
	agofer.partner_name, 
	agofer.amount, 
	agofer.amount_currency,
	--agofer.move_id,
	2316014,
	--agofer.payment_ref
	'False'
FROM dblink('dbname=agofer_08','select
	id,
	statement_id,
	sequence,
	currency_id,
	write_date,
	create_date,
	write_uid,
	partner_id,
	create_uid,
	partner_name,
	amount,
	amount_currency
	from account_bank_statement_line;'
) AS agofer(
	id integer, 
	statement_id integer, 
	sequence integer, 
	currency_id integer, 
	write_date timestamp without time zone, 
	create_date timestamp without time zone, 
	write_uid integer, 
	partner_id integer, 
	create_uid integer, 
	partner_name character varying, 
	amount numeric, 
	amount_currency numeric
);

select setval('account_bank_statement_line_id_seq', (select max(id) from account_bank_statement_line));