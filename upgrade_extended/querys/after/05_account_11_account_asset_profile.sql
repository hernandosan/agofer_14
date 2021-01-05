INSERT INTO account_asset_profile (
	id, 
	method_number, 
	create_date, 
	account_asset_id, 
	account_depreciation_id, 
	company_id, 
	method_time, 
	write_date, 
	write_uid, 
	method_progress_factor, 
	create_uid, 
	account_expense_depreciation_id, 
	name, 
	journal_id, 
	note, 
	prorata, 
	open_asset, 
	method_period, 
	account_analytic_id, 
	method,
	active
) SELECT
	agofer.id, 
	agofer.method_number, 
	agofer.create_date, 
	agofer.account_asset_id, 
	agofer.account_depreciation_id, 
	agofer.company_id, 
	agofer.method_time, 
	agofer.write_date, 
	agofer.write_uid, 
	agofer.method_progress_factor, 
	agofer.create_uid, 
	agofer.account_expense_depreciation_id, 
	agofer.name, 
	agofer.journal_id, 
	agofer.note, 
	agofer.prorata, 
	agofer.open_asset, 
	--agofer.method_period,
	(CASE WHEN agofer.method_period = 1 THEN 'month' WHEN agofer.method_period = 12 THEN 'year' END),
	agofer.account_analytic_id, 
	agofer.method,
	--agofer.active
	TRUE
FROM dblink('dbname=agofer_08','select
	id, 
	method_number, 
	create_date, 
	account_asset_id, 
	account_depreciation_id, 
	company_id, 
	method_time, 
	write_date, 
	write_uid, 
	method_progress_factor, 
	create_uid, 
	account_expense_depreciation_id, 
	name, 
	journal_id, 
	note, 
	prorata, 
	open_asset,
	account_analytic_id, 
	method,
	method_period
	from account_asset_category;'
) AS agofer(
	id integer, 
	method_number integer, 
	create_date timestamp without time zone, 
	account_asset_id integer, 
	account_depreciation_id integer, 
	company_id integer, 
	method_time character varying, 
	write_date timestamp without time zone, 
	write_uid integer, 
	method_progress_factor double precision, 
	create_uid integer, 
	account_expense_depreciation_id integer, 
	name character varying, 
	journal_id integer, 
	note text, 
	prorata boolean, 
	open_asset boolean, 
	account_analytic_id integer,
	method character varying,
	method_period integer
);

select setval('account_asset_profile_id_seq', (select max(id) from account_asset_profile));