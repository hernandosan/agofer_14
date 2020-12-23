INSERT INTO account_analytic_line (
	id,
	create_date,
	account_id,
	write_uid,
	write_date,
	date,
	create_uid,
	user_id,
	name,
	company_id,
	amount,
	unit_amount,
	code,
	general_account_id,
	currency_id,
	move_id,
	product_id,
	product_uom_id,
	ref,
	partner_id
) SELECT
	agofer.id,
	agofer.create_date,
	agofer.account_id,
	agofer.write_uid,
	agofer.write_date,
	agofer.date,
	agofer.create_uid,
	agofer.user_id,
	agofer.name,
	agofer.company_id,
	agofer.amount,
	agofer.unit_amount,
	agofer.code,
	agofer.general_account_id,
	agofer.currency_id,
	agofer.move_id,
	agofer.product_id,
	agofer.product_uom_id,
	agofer.ref,
	agofer.partner_id
FROM dblink('dbname=agofer_08','select
	id,
	create_date,
	account_id,
	write_uid,
	write_date,
	date,
	create_uid,
	user_id,
	name,
	company_id,
	amount,
	unit_amount,
	code,
	general_account_id,
	currency_id,
	move_id,
	product_id,
	product_uom_id,
	ref,
	partner_id
	from account_analytic_line;'
) AS agofer(
	id integer,
	create_date timestamp without time zone,
	account_id integer,
	write_uid integer,
	write_date timestamp without time zone,
	date timestamp without time zone,
	create_uid integer,
	user_id integer,
	name character varying,
	company_id integer,
	amount numeric,
	unit_amount double precision,
	code character varying,
	general_account_id integer,
	currency_id integer,
	move_id integer,
	product_id integer,
	product_uom_id integer,
	ref character varying,
	partner_id integer
)INNER JOIN account_move_line OML ON OML.id = agofer.move_id;

select setval('account_analytic_line_id_seq', (select max(id) from account_analytic_line));