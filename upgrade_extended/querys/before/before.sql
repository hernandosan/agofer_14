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
		where length(name) > 64
		returning id;'
) AS agofer (id INTEGER);

SELECT COUNT(agofer.id)
    FROM dblink('dbname=agofer_08','update
		resource_resource
		set calendar_id = (select id from resource_calendar order by id limit 1)
		where calendar_id is null
		returning id;'
) AS agofer (id INTEGER);

SELECT COUNT(agofer.id)
    FROM dblink('dbname=agofer_08','update procurement_rule set location_id = 1 where location_id is null
		returning id;'
) AS agofer (id INTEGER);

SELECT COUNT(agofer.id)
    FROM dblink('dbname=agofer_08','update procurement_rule set picking_type_id = (select id from stock_picking_type limit 1) where picking_type_id is null
		returning id;'
) AS agofer (id INTEGER);

SELECT COUNT(agofer.id)
    FROM dblink('dbname=agofer_08','update procurement_rule set route_id = 1 where route_id is null
		returning id;'
) AS agofer (id INTEGER);

SELECT COUNT(agofer.id)
    FROM dblink('dbname=agofer_08','update stocK_move set price_unit = cost where price_unit = 0 or price_unit is null
		returning id;'
) AS agofer (id INTEGER);