insert into stock_rule (
	id, 
	create_date, 
	sequence, 
	write_uid, 
	write_date, 
	active, 
	create_uid, 
	name, 
	company_id, 
	action, 
	group_id, 
	group_propagation_option, 
	partner_address_id, 
	warehouse_id, 
	procure_method, 
	location_id, 
	location_src_id, 
	route_sequence, 
	picking_type_id, 
	delay, 
	route_id, 
	propagate_warehouse_id,
	auto
) select 
	agofer.id, 
	agofer.create_date, 
	agofer.sequence, 
	agofer.write_uid, 
	agofer.write_date, 
	agofer.active, 
	agofer.create_uid, 
	agofer.name, 
	agofer.company_id, 
	agofer.action, 
	agofer.group_id, 
	agofer.group_propagation_option, 
	agofer.partner_address_id, 
	--agofer.warehouse_id, 
	null,
	agofer.procure_method, 
	agofer.location_id, 
	agofer.location_src_id, 
	agofer.route_sequence, 
	agofer.picking_type_id, 
	agofer.delay, 
	agofer.route_id, 
	agofer.propagate_warehouse_id,
	'manual'
from dblink('dbname=agofer_08', 'select 
	id, 
	create_date, 
	sequence, 
	write_uid, 
	write_date, 
	active, 
	create_uid, 
	name, 
	company_id, 
	action, 
	group_id, 
	group_propagation_option, 
	partner_address_id, 
	warehouse_id, 
	procure_method, 
	location_id, 
	location_src_id, 
	route_sequence, 
	picking_type_id, 
	delay, 
	route_id, 
	propagate_warehouse_id
	from procurement_rule;'
) as agofer (
	id integer, 
	create_date timestamp without time zone, 
	sequence integer, 
	write_uid integer, 
	write_date timestamp without time zone, 
	active boolean, 
	create_uid integer, 
	name character varying, 
	company_id integer, 
	action character varying, 
	group_id integer, 
	group_propagation_option character varying, 
	partner_address_id integer, 
	warehouse_id integer, 
	procure_method character varying, 
	location_id integer, 
	location_src_id integer, 
	route_sequence numeric, 
	picking_type_id integer, 
	delay integer, 
	route_id integer, 
	propagate_warehouse_id integer
)
where agofer.location_id is not null 
	and agofer.picking_type_id is not null 
	and agofer.route_id is not null 
	and agofer.id not in (select id from stock_rule);