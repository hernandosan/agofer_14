insert into account_account (
	id, 
	code, 
	create_date, 
	reconcile, 
	currency_id, 
	create_uid, 
	write_uid, 
	write_date, 
	name, 
	company_id, 
	note,
	user_type_id
)select 
	agofer.id, 
	agofer.code, 
	agofer.create_date, 
	agofer.reconcile, 
	agofer.currency_id, 
	agofer.create_uid, 
	agofer.write_uid, 
	agofer.write_date, 
	agofer.name, 
	agofer.company_id, 
	agofer.note,
	--agofer.user_type_id
	1
from dblink('dbname=agofer_08','SELECT 
	id, 
	code, 
	create_date, 
	reconcile, 
	currency_id, 
	create_uid, 
	write_uid, 
	write_date, 
	name, 
	company_id, 
	note
	FROM account_account 
	where niif is False;'
) as agofer(
	id integer, 
	code character varying, 
	create_date timestamp without time zone, 
	reconcile boolean, 
	currency_id integer, 
	create_uid integer, 
	write_uid integer, 
	write_date timestamp without time zone, 
	name character varying, 
	company_id integer, 
	note text
)
where agofer.id not in (select id from account_account);
