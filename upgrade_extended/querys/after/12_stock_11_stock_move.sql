insert into stock_move (
	id, 
	origin, 
	create_date, 
	product_uom, 
	price_unit, 
	product_uom_qty, 
	date, 
	product_qty, 
	location_id, 
	note, 
	picking_type_id, 
	partner_id, 
	company_id, 
	priority, 
	state, 
	origin_returned_move_id, 
	create_uid, 
	warehouse_id, 
	inventory_id, 
	restrict_partner_id, 
	procure_method, 
	write_uid, 
	name, 
	rule_id, 
	location_dest_id, 
	write_date, 
	group_id, 
	product_id, 
	picking_id, 
	purchase_line_id, 
	weight, 
	raw_material_production_id, 
	production_id,
	standard_price
) select 
	agofer.id, 
	agofer.origin, 
	agofer.create_date, 
	agofer.product_uom, 
	agofer.price_unit, 
	agofer.product_uom_qty, 
	agofer.date, 
	agofer.product_qty, 
	agofer.location_id, 
	agofer.note, 
	agofer.picking_type_id, 
	agofer.partner_id, 
	agofer.company_id, 
	agofer.priority, 
	agofer.state, 
	--agofer.origin_returned_move_id, 
	null, 
	--agofer.create_uid, 
	2, 
	agofer.warehouse_id, 
	agofer.inventory_id, 
	agofer.restrict_partner_id, 
	agofer.procure_method, 
	--agofer.write_uid, 
	2,
	agofer.name, 
	agofer.rule_id, 
	agofer.location_dest_id, 
	agofer.write_date, 
	agofer.group_id, 
	agofer.product_id, 
	agofer.picking_id, 
	agofer.purchase_line_id, 
	agofer.weight, 
	agofer.raw_material_production_id, 
	agofer.production_id,
	agofer.costo_promedio
from dblink('dbname=agofer_08', 'select 
	id, 
	origin, 
	create_date, 
	product_uom, 
	price_unit, 
	product_uom_qty, 
	date, 
	product_qty, 
	location_id, 
	note, 
	picking_type_id, 
	partner_id, 
	company_id, 
	priority, 
	state, 
	origin_returned_move_id, 
	create_uid, 
	warehouse_id, 
	inventory_id, 
	restrict_partner_id, 
	procure_method, 
	write_uid, 
	name, 
	rule_id, 
	location_dest_id, 
	write_date, 
	group_id, 
	product_id, 
	picking_id, 
	purchase_line_id, 
	weight, 
	raw_material_production_id, 
	production_id,
	costo_promedio
	from stock_move;'
) as agofer (
	id integer, 
	origin character varying, 
	create_date timestamp without time zone, 
	product_uom integer, 
	price_unit double precision, 
	product_uom_qty numeric, 
	date timestamp without time zone, 
	product_qty numeric, 
	location_id integer, 
	note text, 
	picking_type_id integer, 
	partner_id integer, 
	company_id integer, 
	priority character varying, 
	state character varying, 
	origin_returned_move_id integer, 
	create_uid integer, 
	warehouse_id integer, 
	inventory_id integer, 
	restrict_partner_id integer, 
	procure_method character varying, 
	write_uid integer, 
	name character varying, 
	rule_id integer, 
	location_dest_id integer, 
	write_date timestamp without time zone, 
	group_id integer, 
	product_id integer, 
	picking_id integer, 
	purchase_line_id integer, 
	weight numeric, 
	raw_material_production_id integer, 
	production_id integer,
	costo_promedio double precision
)
WHERE CAST(agofer.date as date) >= '2019-01-01';

select setval('stock_move_id_seq', (select max(id) from stock_move));

update stock_move sm 
set location_id = 
case
	when agofer.location_id = 5 then 14 
	when agofer.location_id = 7 then 15 
	else 5 
end
from dblink('dbname=agofer_08','select id, location_id, location_dest_id from stock_move where location_id in (5, 7, 9);') as agofer 
(id integer, location_id integer, location_dest_id integer) 
where agofer.id = sm.id;

update stock_move sm 
set location_dest_id = 
case
	when agofer.location_dest_id = 5 then 14 
	when agofer.location_dest_id = 7 then 15 
	else 5 
end
from dblink('dbname=agofer_08','select id, location_id, location_dest_id from stock_move where location_dest_id in (5, 7, 9);') as agofer 
(id integer, location_id integer, location_dest_id integer) 
where agofer.id = sm.id;