ALTER TABLE stock_location_route DISABLE TRIGGER ALL;
DELETE FROM stock_location_route;
ALTER TABLE stock_location_route ENABLE TRIGGER ALL;

INSERT INTO stock_location_route (
	id, 
	supplier_wh_id, 
	create_uid, 
	create_date, 
	name, 
	sequence, 
	warehouse_selectable, 
	write_date, 
	company_id, 
	supplied_wh_id, 
	product_selectable, 
	product_categ_selectable, 
	active, 
	write_uid, 
	sale_selectable
) SELECT
	agofer.id, 
	agofer.supplier_wh_id, 
	agofer.create_uid, 
	agofer.create_date, 
	agofer.name, 
	agofer.sequence, 
	agofer.warehouse_selectable, 
	agofer.write_date, 
	agofer.company_id, 
	agofer.supplied_wh_id, 
	agofer.product_selectable, 
	agofer.product_categ_selectable, 
	agofer.active, 
	agofer.write_uid, 
	agofer.sale_selectable
FROM dblink('dbname=agofer_08', 'select
	id, 
	supplier_wh_id, 
	create_uid, 
	create_date, 
	name, 
	sequence, 
	warehouse_selectable, 
	write_date, 
	company_id, 
	supplied_wh_id, 
	product_selectable, 
	product_categ_selectable, 
	active, 
	write_uid, 
	sale_selectable
	from stock_location_route'
) AS agofer(
	id integer, 
	supplier_wh_id integer, 
	create_uid integer, 
	create_date timestamp without time zone, 
	name character varying, 
	sequence integer, 
	warehouse_selectable boolean, 
	write_date timestamp without time zone, 
	company_id integer, 
	supplied_wh_id integer, 
	product_selectable boolean, 
	product_categ_selectable boolean, 
	active boolean, 
	write_uid integer, 
	sale_selectable boolean
);

select setval('stock_location_route_id_seq', (select max(id) from stock_location_route));