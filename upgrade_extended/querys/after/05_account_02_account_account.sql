UPDATE account_account SET code = code || '.';

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
	user_type_id
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
	agofer.user_type
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
)
WHERE agofer.type != 'view'
AND agofer.id NOT IN (SELECT id FROM account_account)
AND agofer.code NOT IN (SELECT code FROM account_account);

select setval('account_account_id_seq', (select max(id) from account_account));