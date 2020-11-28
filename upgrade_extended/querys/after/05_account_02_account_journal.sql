insert into account_journal (
	id, 
	code, 
	create_date, 
	write_uid, 
	loss_account_id, 
	write_date, 
	create_uid, 
	name, 
	company_id, 
	profit_account_id, 
	type,
	invoice_reference_type,
	invoice_reference_model,
	active
) select 
	agofer.id, 
	agofer.code, 
	agofer.create_date, 
	agofer.write_uid, 
	agofer.loss_account_id, 
	agofer.write_date, 
	agofer.create_uid, 
	agofer.name, 
	agofer.company_id, 
	agofer.profit_account_id, 
	agofer.type,
	--agofer.invoice_reference_type
	'invoice',
	--agofer.invoice_reference_model
	'odoo',
	--agofer.active
	True
from dblink('dbname=agofer_08','SELECT 
	id, 
	code, 
	create_date, 
	write_uid, 
	loss_account_id, 
	write_date, 
	create_uid, 
	name, 
	company_id, 
	profit_account_id, 
	type,
	name,
	name
	FROM account_journal
	WHERE niif = False;'
) as agofer(
	id integer, 
	code character varying, 
	create_date timestamp without time zone, 
	write_uid integer, 
	loss_account_id integer, 
	write_date timestamp without time zone, 
	create_uid integer, 
	name character varying, 
	company_id integer, 
	profit_account_id integer, 
	type character varying,
	invoice_reference_type character varying,
	invoice_reference_model character varying
);