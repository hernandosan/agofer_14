insert into account_bank_statement_line (
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
)select 
	agofer.id, 
	agofer.statement_id, 
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
	'1921155',
	--agofer.payment_ref
	'False'
from dblink('dbname=agofer_08','SELECT 
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
	FROM account_bank_statement_line
	WHERE statement_id IS NOT null;'
) as agofer(
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
)INNER JOIN account_bank_statement ABS ON ABS.id = agofer.statement_id
where cast(agofer.create_date as date) >= '2019-01-01';

select setval('account_bank_statement_line_id_seq', (select max(id) from account_bank_statement_line));

update account_move_line aml
set statement_line_id = agofer.statement_line_id
from dblink('dbname=agofer_08','SELECT id, statement_line_id FROM account_move_line;') as agofer
(id integer, statement_line_id integer)
inner join account_bank_statement_line abs on agofer.statement_line_id = abs.id
where agofer.id = aml.id;