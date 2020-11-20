insert into account_tax (
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
) select 
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
from dblink('dbname=agofer_08','SELECT 
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
	FROM account_tax;'
) as agofer(
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
);

