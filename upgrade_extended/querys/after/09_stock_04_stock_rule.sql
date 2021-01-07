ALTER TABLE stock_rule DISABLE TRIGGER ALL;
DELETE FROM stock_rule;
ALTER TABLE stock_rule ENABLE TRIGGER ALL;

INSERT INTO stock_rule (
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
	propagate_cancel, 
	auto
) SELECT
	agofer.id, 
	agofer.create_date, 
	agofer.sequence, 
	agofer.write_uid, 
	agofer.write_date, 
	agofer.active, 
	agofer.create_uid, 
	agofer.name, 
	agofer.company_id, 
	--agofer.action, 
	case when agofer.action = 'move' then 'pull' else agofer.action end, 
	agofer.group_id, 
	agofer.group_propagation_option, 
	agofer.partner_address_id, 
	-- agofer.warehouse_id, 
	1, 
	agofer.procure_method, 
	agofer.location_id, 
	agofer.location_src_id, 
	agofer.route_sequence, 
	agofer.picking_type_id, 
	agofer.delay, 
	agofer.route_id, 
	agofer.propagate_warehouse_id,
	agofer.propagate,
	--agofer.auto 
	'manual'
FROM dblink('dbname=agofer_08', 'select
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
	propagate
	from procurement_rule 
	where route_id is not null 
	and picking_type_id is not null 
	and location_id is not null;'
) AS agofer (
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
	propagate_warehouse_id integer,
	propagate boolean
);

select setval('stock_rule_id_seq', (select max(id) from stock_rule));