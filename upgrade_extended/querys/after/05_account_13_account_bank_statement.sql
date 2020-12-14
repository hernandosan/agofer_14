insert into account_bank_statement(
	id, 
	create_date, 
	write_uid, 
	balance_start, 
	company_id, 
	total_entry_encoding, 
	write_date, 
	date, 
	create_uid, 
	user_id, 
	name, 
	balance_end, 
	journal_id, 
	state, 
	balance_end_real
)select 
	agofer.id, 
	agofer.create_date, 
	agofer.write_uid, 
	agofer.balance_start, 
	agofer.company_id, 
	agofer.total_entry_encoding, 
	agofer.write_date, 
	agofer.date, 
	agofer.create_uid, 
	agofer.user_id, 
	agofer.name, 
	agofer.balance_end, 
	agofer.journal_id, 
	agofer.state, 
	agofer.balance_end_real
from dblink('dbname=agofer_08','SELECT 
	id, 
	create_date, 
	write_uid, 
	balance_start, 
	company_id, 
	total_entry_encoding, 
	write_date, 
	date, 
	create_uid, 
	user_id, 
	name, 
	balance_end, 
	journal_id, 
	state, 
	balance_end_real
	FROM account_bank_statement;'
) as agofer(
	id integer, 
	create_date timestamp without time zone, 
	write_uid integer, 
	balance_start numeric, 
	company_id integer, 
	total_entry_encoding numeric, 
	write_date timestamp without time zone, 
	date date, 
	create_uid integer, 
	user_id integer, 
	name character varying, 
	balance_end numeric, 
	journal_id integer, 
	state character varying, 
	balance_end_real numeric
)INNER JOIN account_journal AJ ON AJ.id = agofer.journal_id;

select setval('account_bank_statement_id_seq', (select max(id) from account_bank_statement));

update account_move_line aml
set statement_id = agofer.statement_id
from dblink('dbname=agofer_08','SELECT id, statement_id FROM account_move_line;') as agofer
(id integer, statement_id integer)
inner join account_bank_statement abs on agofer.statement_id = abs.id
where agofer.id = aml.id;