insert into account_payment_term_line (
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
)
select 
	agofer.id, 
	agofer.payment_id, 
	agofer.create_uid, 
	agofer.create_date, 
	agofer.days, 
	agofer.value, 
	agofer.write_uid, 
	agofer.write_date, 
	agofer.value_amount,
	'day_after_invoice_date'
from dblink('dbname=agofer_08',
            'select 
	id, 
	payment_id, 
	create_uid, 
	create_date, 
	days, 
	value, 
	write_uid, 
	write_date, 
	value_amount
from account_payment_term_line;') as agofer(
	id integer, 
	payment_id integer, 
	create_uid integer, 
	create_date timestamp without time zone, 
	days integer, 
	value character varying, 
	write_uid integer, 
	write_date timestamp without time zone, 
	value_amount numeric
) where agofer.id not in (select id from account_payment_term_line);;

select setval('account_payment_term_line_id_seq', (select max(id) from account_payment_term_line));