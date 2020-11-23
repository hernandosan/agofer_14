-- update res_partner set title = null where title > 5;

-- update procurement_rule pr
-- set warehouse_id = sw.id
-- from stock_warehouse sw
-- where sw.code = split_part(pr.name, ':', 1)  
-- and pr.warehouse_id is null;

-- update procurement_rule pr
-- set location_id = sw.lot_stock_id
-- from stock_warehouse sw
-- where sw.id = pr.warehouse_id
-- and pr.location_id is null;

-- update procurement_rule pr
-- set picking_type_id = sw.out_type_id
-- from stock_warehouse sw
-- where sw.id = pr.warehouse_id  
-- and pr.picking_type_id is null;

-- update purchase_order set incoterm_id = null where incoterm_id > 11;

-- update sale_order set incoterm = null where incoterm > 11;

--ALTER USER odoo WITH SUPERUSER;

--create extension dblink;

select count(agofer.id)
dblink('dbname=agofer_08', 'update res_partner set title = null where title > 5 returning id;') as agofer(id integer);
