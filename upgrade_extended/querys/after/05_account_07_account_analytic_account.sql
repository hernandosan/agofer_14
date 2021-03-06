INSERT INTO account_analytic_account (
	id, 
	code, 
	create_date, 
	write_uid, 
	write_date, 
	partner_id, 
	create_uid, 
	name, 
	company_id,
	active
) SELECT
	agofer.id, 
	agofer.code, 
	agofer.create_date, 
	agofer.write_uid, 
	agofer.write_date, 
	agofer.partner_id, 
	agofer.create_uid, 
	agofer.name, 
	agofer.company_id,
	--agofer.active
	TRUE
FROM dblink('dbname=agofer_08','SELECT
	id, 
	code, 
	create_date, 
	write_uid, 
	write_date, 
	partner_id, 
	create_uid, 
	name, 
	company_id
	FROM account_analytic_account;'
) AS agofer(
	id integer, 
	code character varying, 
	create_date timestamp without time zone, 
	write_uid integer, 
	write_date timestamp without time zone, 
	partner_id integer, 
	create_uid integer, 
	name character varying, 
	company_id integer
);

select setval('account_analytic_account_id_seq', (select max(id) from account_analytic_account));