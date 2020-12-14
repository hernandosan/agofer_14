insert into stock_move_line (
	id, 
	create_date, 
	result_package_id, 
	write_uid, 
	package_id, 
	write_date, 
	product_qty, 
	product_uom_qty,
	date, 
	lot_id, 
	location_id, 
	create_uid, 
	product_id, 
	product_uom_id, 
	location_dest_id, 
	qty_done, 
	picking_id, 
	owner_id,
	company_id
) select 
	agofer.id, 
	agofer.create_date, 
	agofer.result_package_id, 
	agofer.write_uid, 
	agofer.package_id, 
	agofer.write_date, 
	agofer.product_qty, 
	agofer.product_qty,
	agofer.date, 
	agofer.lot_id, 
	agofer.location_id, 
	agofer.create_uid, 
	agofer.product_id, 
	agofer.product_uom_id, 
	agofer.location_dest_id, 
	agofer.qty_done, 
	agofer.picking_id, 
	agofer.owner_id,
	1
from dblink('dbname=agofer_08','select 
	id, 
	create_date, 
	result_package_id, 
	write_uid, 
	package_id, 
	write_date, 
	product_qty, 
	date, 
	lot_id, 
	location_id, 
	create_uid, 
	product_id, 
	product_uom_id, 
	location_dest_id, 
	qty_done, 
	picking_id, 
	owner_id
from stock_pack_operation;'
) as agofer(
	id integer, 
	create_date timestamp without time zone, 
	result_package_id integer, 
	write_uid integer, 
	package_id integer, 
	write_date timestamp without time zone, 
	product_qty numeric, 
	date timestamp without time zone, 
	lot_id integer, 
	location_id integer, 
	create_uid integer, 
	product_id integer, 
	product_uom_id integer, 
	location_dest_id integer, 
	qty_done numeric, 
	picking_id integer, 
	owner_id integer
)
inner join stock_picking sp on sp.id = agofer.picking_id;

select setval('stock_move_line_id_seq', (select max(id) from stock_move_line));

update stock_move_line sml 
set move_id = agofer.move_id
from dblink('dbname=agofer_08','select spo.id, sm.id as move_id
from stock_pack_operation spo
inner join stock_move sm on sm.picking_id = spo.picking_id and sm.product_id = spo.product_id;') as agofer (id integer, move_id integer) 
inner join stock_move sm on sm.id = agofer.move_id
where agofer.id = sml.id;