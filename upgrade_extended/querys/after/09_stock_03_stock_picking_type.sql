ALTER TABLE stock_picking_type DISABLE TRIGGER ALL;
DELETE FROM stock_picking_type;
ALTER TABLE stock_picking_type ENABLE TRIGGER ALL;

INSERT INTO stock_picking_type (
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
	company_id,
	show_entire_packs
) select 
	agofer.id, 
	agofer.code, 
	agofer.create_date, 
	agofer.write_date, 
	agofer.sequence, 
	agofer.color, 
	--agofer.warehouse_id,
	1,
	agofer.sequence_id, 
	agofer.active, 
	agofer.write_uid, 
	agofer.create_uid, 
	agofer.default_location_dest_id, 
	agofer.name, 
	agofer.return_picking_type_id, 
	agofer.default_location_src_id,
	--agofer.sequence_code
	'UNK',
	--agofer.company_id
	1,
	--agofer.show_entire_packs
	True
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
) AS agofer (
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

select setval('stock_picking_type_id_seq', (select max(id) from stock_picking_type));