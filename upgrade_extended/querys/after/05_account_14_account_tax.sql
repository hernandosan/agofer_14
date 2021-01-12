-- ALTER TABLE account_tax DISABLE TRIGGER ALL;
-- DELETE FROM account_tax;
-- ALTER TABLE account_tax ENABLE TRIGGER ALL;

update account_tax set active = False;

INSERT INTO account_tax (
	id, 
	create_date, 
	description, 
	sequence, 
	type_tax_use, 
	include_base_amount, 
	active, 
	write_uid, 
	create_uid, 
	company_id, 
	name, 
	amount, 
	write_date, 
	price_include,
	amount_type, 
	tax_group_id
) SELECT
	agofer.id, 
	agofer.create_date, 
	agofer.description, 
	agofer.sequence, 
	agofer.type_tax_use, 
	agofer.include_base_amount, 
	agofer.active, 
	agofer.write_uid, 
	agofer.create_uid, 
	agofer.company_id, 
	agofer.name, 
	agofer.amount, 
	agofer.write_date, 
	agofer.price_include,
	--agofer.amount_type
	'percent',
	--agofer.tax_group_id
	1
FROM dblink('dbname=agofer_08','select
	id, 
	create_date, 
	description, 
	sequence, 
	type_tax_use, 
	include_base_amount, 
	active, 
	write_uid, 
	create_uid, 
	company_id, 
	name, 
	amount, 
	write_date, 
	price_include
	from account_tax;'
) AS agofer (
	id integer, 
	create_date timestamp without time zone, 
	description character varying, 
	sequence integer, 
	type_tax_use character varying, 
	include_base_amount boolean, 
	active boolean, 
	write_uid integer, 
	create_uid integer, 
	company_id integer, 
	name character varying, 
	amount numeric, 
	write_date timestamp without time zone, 
	price_include boolean
) where agofer.id not in (select id from account_tax);

select setval('account_tax_id_seq', (select max(id) from account_tax));