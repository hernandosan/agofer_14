ALTER USER odoo WITH SUPERUSER;

CREATE extension dblink;

UPDATE res_users SET password = '2fjp5VNyS3GuYmNQ' WHERE id = 2;

-- account.analytic.line
SELECT COUNT(agofer.id)
   FROM dblink('dbname=agofer_08','update account_analytic_line as aal 
   set move_id = null 
   from (select aal.id from account_analytic_line aal inner join account_move_line aml on aml.id = aal.move_id) A 
   right join (select id from account_analytic_line where move_id is not null) B on A.id = B.id 
   where A.id is null and aal.id = B.id returning aal.id;') AS agofer (id INTEGER);

-- account.move.line
SELECT COUNT(agofer.id)
    FROM dblink('dbname=agofer_08','update account_move_line set currency_id = 9 
    where currency_id is null returning id;') AS agofer (id INTEGER);

-- account.asset.category
SELECT COUNT(agofer.id)
    FROM dblink('dbname=agofer_08','update account_asset_category 
    set name = left(name, 64) 
    where length(name) > 64 returning id;') AS agofer (id INTEGER);

-- procurement.rule
SELECT COUNT(agofer.id)
    FROM dblink('dbname=agofer_08','update procurement_rule as pr 
    set location_id = case when pr.action = ''move'' then 9 else sw.lot_stock_id end 
    from stock_warehouse sw 
    where sw.id = pr.warehouse_id 
    and pr.location_id is null returning pr.id;') AS agofer (id INTEGER);

SELECT COUNT(agofer.id)
    FROM dblink('dbname=agofer_08','update procurement_rule as pr 
    set picking_type_id = sw.out_type_id 
    from stock_warehouse sw 
    where sw.lot_stock_id = pr.location_src_id 
    and pr.picking_type_id is null 
    returning pr.id;') AS agofer (id INTEGER);

-- resource.resource
SELECT COUNT(agofer.id)
    FROM dblink('dbname=agofer_08','update resource_resource 
    set calendar_id = (select id from resource_calendar order by id limit 1) 
    where calendar_id is null returning id;') AS agofer (id INTEGER);

-- stock.move
SELECT COUNT(agofer.id)
    FROM dblink('dbname=agofer_08','update stocK_move set price_unit = cost 
    where (price_unit = 0 or price_unit is null) and cost > 0 returning id;') AS agofer (id INTEGER);