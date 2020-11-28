insert into stock_picking_type (
	id, 
	code, 
	create_date, 
	write_date, 
	sequence, 
	color, 
	warehouse_id, 
	sequence_id, 
	active, 
	write_uid, 
	create_uid, 
	default_location_dest_id, 
	name, 
	return_picking_type_id, 
	default_location_src_id, 
	sequence_code,
	company_id
) select 
	agofer.id, 
	agofer.code, 
	agofer.create_date, 
	agofer.write_date, 
	agofer.sequence, 
	agofer.color, 
	--agofer.warehouse_id, 
	null,
	agofer.sequence_id, 
	agofer.active, 
	agofer.write_uid, 
	agofer.create_uid, 
	agofer.default_location_dest_id, 
	agofer.name, 
	agofer.return_picking_type_id, 
	agofer.default_location_src_id, 
	'UNK',
	1
from dblink('dbname=agofer_08', 'select
	id, 
	code, 
	create_date, 
	write_date, 
	sequence, 
	color, 
	warehouse_id, 
	sequence_id, 
	active, 
	write_uid, 
	create_uid, 
	default_location_dest_id, 
	name, 
	return_picking_type_id, 
	default_location_src_id
	from stock_picking_type;'
) as agofer (
	id integer, 
	code character varying, 
	create_date timestamp without time zone, 
	write_date timestamp without time zone, 
	sequence integer, 
	color integer, 
	warehouse_id integer, 
	sequence_id integer, 
	active boolean, 
	write_uid integer, 
	create_uid integer, 
	default_location_dest_id integer, 
	name character varying, 
	return_picking_type_id integer, 
	default_location_src_id integer
);