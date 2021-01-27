INSERT INTO stock_picking (
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
	warehouse_id,
	carrier_tracking_ref,
	carrier_id,
	weight,
	incoterm,
	sale_id,
	printed,
	upload_date,
	delivery_bool,
	pick_bool,
	pick_date,
	delivery_date,
	location_id,
    location_dest_id,
	scheduled_date
) SELECT
	agofer.id,
	agofer.origin,
	agofer.owner_id,
	agofer.create_date,
	--agofer.backorder_id,
	null,
	agofer.date_done,
	agofer.create_uid,
	agofer.company_id,
	agofer.write_date,
	agofer.date,
	agofer.write_uid,
	agofer.note,
	agofer.group_id,
	agofer.picking_type_id,
	agofer.partner_id,
	agofer.move_type,
	agofer.name,
	agofer.priority,
	agofer.state,
	agofer.warehouse_id,
	agofer.carrier_tracking_ref,
	--agofer.carrier_id,
	(CASE WHEN agofer.carrier_id = 2 then 1 ELSE agofer.carrier_id end),
	agofer.weight,
	agofer.incoterm,
	--agofer.sale_id,
	null,
	agofer.printed,
	agofer.upload_date,
	agofer.delivery_bool,
	agofer.pick_bool,
	agofer.pick_date,
	agofer.delivery_date,
	--agofer.location_id,
    1,
    --agofer.location_dest_id
    1,
	agofer.date
FROM dblink('dbname=agofer_08', 'select
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
	warehouse_id,
	carrier_tracking_ref,
	carrier_id,
	weight,
	incoterm,
	sale_id,
	printed,
	upload_date,
	delivery_bool,
	pick_bool,
	pick_date,
	delivery_date
	from stock_picking;'
) AS agofer (
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
	warehouse_id integer,
	carrier_tracking_ref character varying,
	carrier_id integer,
	weight numeric,
	incoterm integer,
	sale_id integer,
	printed boolean,
	upload_date date,
	delivery_bool boolean,
	pick_bool boolean,
	pick_date date,
	delivery_date date
);

select setval('stock_picking_id_seq', (select max(id) from stock_picking));

update stock_move as sm 
set reference = sp.name 
from stock_picking sp 
where sp.id = sm.picking_id 
and sm.reference is null;