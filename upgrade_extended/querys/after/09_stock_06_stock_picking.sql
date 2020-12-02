insert into stock_picking (
	id, 
	origin, 
	owner_id, 
	create_date, 
	backorder_id, 
	date_done, 
	create_uid, 
	company_id, 
	write_date, 
	date, 
	write_uid, 
	note, 
	group_id, 
	picking_type_id, 
	partner_id, 
	move_type, 
	name, 
	priority, 
	state, 
	carrier_tracking_ref, 
	carrier_id, 
	weight, 
	location_id,
	location_dest_id,
	shipping_type,
	upload_date,
	delivery_date,
	pick_date
) select 
	agofer.id, 
	agofer.origin, 
	agofer.owner_id, 
	agofer.create_date, 
	agofer.backorder_id, 
	agofer.date_done, 
	agofer.create_uid, 
	agofer.company_id, 
	agofer.write_date, 
	agofer.date, 
	--agofer.write_uid, 
	2,
	agofer.note, 
	agofer.group_id, 
	agofer.picking_type_id, 
	agofer.partner_id, 
	agofer.move_type, 
	agofer.name, 
	agofer.priority, 
	agofer.state, 
	agofer.carrier_tracking_ref, 
	agofer.carrier_id, 
	agofer.weight,
	--location_id,
	--location_dest_id,
	1,
	1,
	agofer.op_condition,
	agofer.upload_date,
	agofer.delivery_date,
	agofer.pick_date
from dblink('dbname=agofer_08', 'select 
	id, 
	origin, 
	owner_id, 
	create_date, 
	backorder_id, 
	date_done, 
	create_uid, 
	company_id, 
	write_date, 
	date, 
	write_uid, 
	note, 
	group_id, 
	picking_type_id, 
	partner_id, 
	move_type, 
	name, 
	priority, 
	state, 
	carrier_tracking_ref, 
	carrier_id, 
	weight,
	op_condition,
	upload_date,
	delivery_date,
	pick_date
	from stock_picking;'
) as agofer (
	id integer, 
	origin character varying, 
	owner_id integer, 
	create_date timestamp without time zone, 
	backorder_id integer, 
	date_done timestamp without time zone, 
	create_uid integer, 
	company_id integer, 
	write_date timestamp without time zone, 
	date timestamp without time zone, 
	write_uid integer, 
	note text, 
	group_id integer, 
	picking_type_id integer, 
	partner_id integer, 
	move_type character varying, 
	name character varying, 
	priority character varying, 
	state character varying, 
	carrier_tracking_ref character varying, 
	carrier_id integer, 
	weight numeric,
	op_condition character varying,
	upload_date date,
	delivery_date date,
	pick_date date
)
INNER JOIN delivery_carrier DC ON DC.id = agofer.carrier_id
INNER JOIN stock_picking SP ON SP.id = agofer.backorder_id;