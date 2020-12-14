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
	--agofer.carrier_id, 
	null,
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
);

select setval('stock_picking_id_seq', (select max(id) from stock_picking));

update stock_picking as sp 
set sale_id = so.id
from procurement_group pg
inner join sale_order so on so.name = pg.name 
where pg.id = sp.group_id;

update stock_picking as sp 
set location_id = sm.location_id,
location_dest_id = sm.location_dest_id
from stock_move sm 
where sm.picking_id = sp.id;

update stock_picking set scheduled_date = date where scheduled_date is null;

update stock_picking set shipping_type = null where sale_id is null;

update stock_picking as sp 
set shipping_type = null 
from stock_picking_type spt 
where spt.id = sp.picking_type_id 
and spt.code != 'outgoing' 
and sp.shipping_type is not null;

update stock_picking set delivery_bool = True where shipping_type = 'delivery' and delivery_date is null;

update stock_picking set delivery_bool = True where shipping_type = 'pick' and pick_date is null;