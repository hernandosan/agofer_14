insert into account_asset_line (
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
) select 
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
from dblink('dbname=agofer_08','SELECT 
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
	FROM account_asset_depreciation_line;'
) as agofer(
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
)
INNER JOIN account_asset AA ON AA.id = agofer.asset_id
INNER JOIN account_move AM ON AM.id = agofer.move_id;