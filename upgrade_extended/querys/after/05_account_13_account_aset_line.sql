INSERT INTO account_asset_line (
	id, 
	asset_id, 
	create_uid, 
	create_date, 
	name, 
	move_check, 
	amount, 
	write_date, 
	write_uid, 
	remaining_value, 
	move_id, 
	depreciated_value,
	line_date
) SELECT
	agofer.id, 
	agofer.asset_id, 
	agofer.create_uid, 
	agofer.create_date, 
	agofer.name, 
	agofer.move_check, 
	agofer.amount, 
	agofer.write_date, 
	agofer.write_uid, 
	agofer.remaining_value, 
	agofer.move_id, 
	agofer.depreciated_value,
	agofer.depreciation_date
FROM dblink('dbname=agofer_08','select
	id, 
	asset_id, 
	create_uid, 
	create_date, 
	name, 
	move_check, 
	amount, 
	write_date, 
	write_uid, 
	remaining_value, 
	move_id, 
	depreciated_value,
	depreciation_date
	from account_asset_depreciation_line;'
) AS agofer(
	id integer, 
	asset_id integer, 
	create_uid integer, 
	create_date timestamp without time zone, 
	name character varying, 
	move_check boolean, 
	amount numeric, 
	write_date timestamp without time zone, 
	write_uid integer, 
	remaining_value numeric, 
	move_id integer, 
	depreciated_value double precision,
	depreciation_date date
);

select setval('account_asset_line_id_seq', (select max(id) from account_asset_line));