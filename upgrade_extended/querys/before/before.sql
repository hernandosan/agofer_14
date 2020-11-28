ALTER USER odoo WITH SUPERUSER;

CREATE extension dblink;

SELECT COUNT(agofer.id)
    FROM dblink('dbname=agofer_08', 'update
		res_partner
		set title = null
		where title > 5
		returning id;'
) AS agofer (id INTEGER);

SELECT COUNT(agofer.id)
    FROM dblink('dbname=agofer_08', 'update
		procurement_rule pr
		set warehouse_id = sw.id
		from stock_warehouse sw
		where sw.code = split_part(pr.name, '':'', 1)
		and pr.warehouse_id is null
		returning pr.id;'
) as agofer (id integer);

SELECT COUNT(agofer.id)
    FROM dblink('dbname=agofer_08', 'update
		procurement_rule pr
		set location_id = sw.lot_stock_id
		from stock_warehouse sw
		where sw.id = pr.warehouse_id
		and pr.location_id is null
		returning pr.id;'
) as agofer (id integer);

SELECT COUNT(agofer.id)
    FROM dblink('dbname=agofer_08','update
		procurement_rule pr
		set picking_type_id = sw.out_type_id
		from stock_warehouse sw
		where sw.id = pr.warehouse_id
		and pr.picking_type_id is null
		returning pr.id;'
) as agofer (id integer);

SELECT COUNT(agofer.id)
    FROM dblink('dbname=agofer_08','update
		purchase_order
		set incoterm_id = null
		where incoterm_id > 11
		returning id;'
) AS agofer (id INTEGER);

SELECT COUNT(agofer.id)
    FROM dblink('dbname=agofer_08','update
		sale_order
		set incoterm = null
		where incoterm > 11
		returning id;'
) AS agofer (id INTEGER);

SELECT COUNT(agofer.id)
    FROM dblink('dbname=agofer_08','update
		account_asset_category
		set name = left(name, 64)
		returning id;'
) AS agofer (id INTEGER);
