insert into account_payment_term (
	id, 
	create_uid, 
	create_date, 
	name, 
	write_uid, 
	note, 
	write_date, 
	active,
	sequence)
	select agofer.id, 
	agofer.create_uid, 
	agofer.create_date, 
	agofer.name, 
	agofer.write_uid, 
	agofer.note, 
	agofer.write_date, 
	agofer.active,
	10
from dblink('dbname=agofer_08', 'select 
	id, 
	create_uid, 
	create_date, 
	name, 
	write_uid, 
	note, 
	write_date, 
	active from account_payment_term;'
) as agofer(
	id integer, 
	create_uid integer, 
	create_date timestamp without time zone, 
	name character varying, 
	write_uid integer, 
	note text, 
	write_date timestamp without time zone, 
	active boolean) 
where agofer.id not in (select id from account_payment_term);

select setval('account_payment_term_id_seq', (select max(id) from account_payment_term));