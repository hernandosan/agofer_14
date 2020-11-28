insert into account_asset (
	id, 
	method_number, 
	code, 
	create_date, 
	method_end, 
	prorata, 
	salvage_value, 
	write_uid, 
	method_time, 
	write_date, 
	active, 
	partner_id, 
	name, 
	create_uid, 
	method_progress_factor, 
	purchase_value, 
	company_id, 
	note, 
	state, 
	method_period, 
	method, 
	value_residual,
	profile_id,
	date_start
) select 
	agofer.id, 
	agofer.method_number, 
	agofer.code, 
	agofer.create_date, 
	agofer.method_end, 
	agofer.prorata, 
	agofer.salvage_value, 
	agofer.write_uid, 
	agofer.method_time, 
	agofer.write_date, 
	agofer.active, 
	agofer.partner_id, 
	agofer.name, 
	agofer.create_uid, 
	agofer.method_progress_factor, 
	agofer.purchase_value, 
	agofer.company_id, 
	agofer.note, 
	agofer.state, 
	agofer.method_period, 
	agofer.method, 
	agofer.value_residual,
	agofer.category_id,
	agofer.purchase_date
from dblink('dbname=agofer_08','SELECT 
	id, 
	method_number, 
	code, 
	create_date, 
	method_end, 
	prorata, 
	salvage_value, 
	write_uid, 
	method_time, 
	write_date, 
	active, 
	partner_id, 
	name, 
	create_uid, 
	method_progress_factor, 
	purchase_value, 
	company_id, 
	note, 
	state, 
	method_period, 
	method, 
	value_residual,
	category_id,
	purchase_date
	FROM account_asset_asset;'
) as agofer(
	id integer, 
	method_number integer, 
	code character varying, 
	create_date timestamp without time zone, 
	method_end date, 
	prorata boolean, 
	salvage_value numeric, 
	write_uid integer, 
	method_time character varying, 
	write_date timestamp without time zone, 
	active boolean, 
	partner_id integer, 
	name character varying, 
	create_uid integer, 
	method_progress_factor double precision, 
	purchase_value double precision, 
	company_id integer, 
	note text, 
	state character varying, 
	method_period integer, 
	method character varying, 
	value_residual numeric,
	category_id integer,
	purchase_date date
)INNER JOIN account_asset_profile AAP ON AAP.id = agofer.category_id;