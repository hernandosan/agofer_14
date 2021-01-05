ALTER USER odoo WITH SUPERUSER;

CREATE extension dblink;

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

--SELECT COUNT(agofer.id)
--    FROM dblink('dbname=agofer_08','update account_analytic_line as aal set move_id = null from (select aal.id from account_analytic_line aal inner join account_move_line aml on aml.id = aal.move_id) A
--right join (select id from account_analytic_line where move_id is not null) B on A.id = B.id where A.id is null and aal.id = B.id;'
--) AS agofer (id INTEGER);
