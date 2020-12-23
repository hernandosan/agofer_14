ALTER TABLE stock_warehouse DISABLE TRIGGER ALL;
DELETE FROM stock_warehouse;
ALTER TABLE stock_warehouse ENABLE TRIGGER ALL;

INSERT INTO stock_warehouse (
	id, 
	mto_pull_id, 
	code, 
	create_date, 
	lot_stock_id, 
	wh_pack_stock_loc_id, 
	pack_type_id, 
	reception_route_id, 
	pick_type_id, 
	crossdock_route_id, 
	write_uid, 
	write_date, 
	delivery_route_id, 
	partner_id, 
	name, 
	create_uid, 
	wh_qc_stock_loc_id, 
	wh_output_stock_loc_id, 
	in_type_id, 
	company_id, 
	out_type_id, 
	int_type_id, 
	wh_input_stock_loc_id, 
	delivery_steps, 
	reception_steps, 
	view_location_id, 
	buy_pull_id, 
	buy_to_resupply, 
	manufacture_pull_id, 
	manufacture_to_resupply,
	manufacture_steps,
	active
) SELECT
	agofer.id, 
	--agofer.mto_pull_id, 
	null,
	agofer.code, 
	agofer.create_date, 
	agofer.lot_stock_id, 
	agofer.wh_pack_stock_loc_id, 
	agofer.pack_type_id, 
	agofer.reception_route_id, 
	agofer.pick_type_id, 
	agofer.crossdock_route_id, 
	agofer.write_uid, 
	agofer.write_date, 
	agofer.delivery_route_id, 
	agofer.partner_id, 
	agofer.name, 
	agofer.create_uid, 
	agofer.wh_qc_stock_loc_id, 
	agofer.wh_output_stock_loc_id, 
	agofer.in_type_id, 
	agofer.company_id, 
	agofer.out_type_id, 
	agofer.int_type_id, 
	agofer.wh_input_stock_loc_id, 
	agofer.delivery_steps, 
	agofer.reception_steps, 
	agofer.view_location_id, 
	agofer.buy_pull_id, 
	agofer.buy_to_resupply, 
	agofer.manufacture_pull_id, 
	agofer.manufacture_to_resupply,
	--agofer.manufacture_steps
	'mrp_one_step',
	--agofer.active
	TRUE
FROM dblink('dbname=agofer_08', 'select
	id, 
	mto_pull_id, 
	code, 
	create_date, 
	lot_stock_id, 
	wh_pack_stock_loc_id, 
	pack_type_id, 
	reception_route_id, 
	pick_type_id, 
	crossdock_route_id, 
	write_uid, 
	write_date, 
	delivery_route_id, 
	partner_id, 
	name, 
	create_uid, 
	wh_qc_stock_loc_id, 
	wh_output_stock_loc_id, 
	in_type_id, 
	company_id, 
	out_type_id, 
	int_type_id, 
	wh_input_stock_loc_id, 
	delivery_steps, 
	reception_steps, 
	view_location_id, 
	buy_pull_id, 
	buy_to_resupply, 
	manufacture_pull_id, 
	manufacture_to_resupply
	from stock_warehouse;'
) AS agofer (
	id integer, 
	mto_pull_id integer, 
	code character varying, 
	create_date timestamp without time zone, 
	lot_stock_id integer, 
	wh_pack_stock_loc_id integer, 
	pack_type_id integer, 
	reception_route_id integer, 
	pick_type_id integer, 
	crossdock_route_id integer, 
	write_uid integer, 
	write_date timestamp without time zone, 
	delivery_route_id integer, 
	partner_id integer, 
	name character varying, 
	create_uid integer, 
	wh_qc_stock_loc_id integer, 
	wh_output_stock_loc_id integer, 
	in_type_id integer, 
	company_id integer, 
	out_type_id integer, 
	int_type_id integer, 
	wh_input_stock_loc_id integer, 
	delivery_steps character varying, 
	reception_steps character varying, 
	view_location_id integer, 
	buy_pull_id integer, 
	buy_to_resupply boolean, 
	manufacture_pull_id integer, 
	manufacture_to_resupply boolean
) 
WHERE agofer.id NOT IN (SELECT id FROM stock_warehouse);

select setval('stock_warehouse_id_seq', (select max(id) from stock_warehouse));