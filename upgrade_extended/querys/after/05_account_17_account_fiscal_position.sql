INSERT INTO account_fiscal_position (
	id,
	create_uid,
	country_group_id,
	create_date,
	name,
	sequence,
	country_id,
	company_id,
	auto_apply,
	write_uid,
	note,
	write_date,
	vat_required,
	active
) SELECT
	agofer.id,
	agofer.create_uid,
	agofer.country_group_id,
	agofer.create_date,
	agofer.name,
	agofer.sequence,
	agofer.country_id,
	agofer.company_id,
	agofer.auto_apply,
	agofer.write_uid,
	agofer.note,
	agofer.write_date,
	agofer.vat_required,
	agofer.active
FROM dblink('dbname=agofer_08','select
	id,
	create_uid,
	country_group_id,
	create_date,
	name,
	sequence,
	country_id,
	company_id,
	auto_apply,
	write_uid,
	note,
	write_date,
	vat_required,
	active
	from account_fiscal_position;'
) AS agofer(
	id integer,
	create_uid integer,
	country_group_id integer,
	create_date timestamp without time zone,
	name character varying,
	sequence integer,
	country_id integer,
	company_id integer,
	auto_apply boolean,
	write_uid integer,
	note text,
	write_date timestamp without time zone,
	vat_required boolean,
	active boolean
);

select setval('account_fiscal_position_id_seq', (select max(id) from account_fiscal_position));