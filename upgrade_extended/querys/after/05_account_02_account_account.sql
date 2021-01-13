-- ALTER TABLE account_account DISABLE TRIGGER ALL;
-- DELETE FROM account_account;
-- ALTER TABLE account_account ENABLE TRIGGER ALL;

update account_account set active = False, code = code || '.';

INSERT INTO account_account (
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
	user_type_id,
	active
) SELECT
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
	agofer.user_type,
	True
FROM dblink('dbname=agofer_08','SELECT
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
	type,
	user_type
	FROM account_account;'
) AS agofer (
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
	note text,
	type character varying,
	user_type integer
) where agofer.id not in (select id from account_account);

select setval('account_account_id_seq', (select max(id) from account_account));

update account_account as aa 
set internal_type = aat.type
from account_account_type aat 
where aat.id = aa.user_type_id;