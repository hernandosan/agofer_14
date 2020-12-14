-- insert into account_group (name, company_id, niif_bool)
-- select left(code, -2), 1, False from account_account group by left(code, -2);

-- insert into account_group (name, company_id, niif_bool) 
-- select left(code, -4), 1, False from account_account group by left(code, -4);

-- insert into account_group (name, company_id, niif_bool) 
-- select left(code, -6), 1, False from account_account group by left(code, -6);

-- insert into account_group (name, company_id, niif_bool) 
-- select left(code, -8), 1, False from account_account group by left(code, -8);

-- insert into account_group (name, company_id, niif_bool) 
-- select left(code, -10), 1, False from account_account group by left(code, -10);

delete from account_group where name = '';

-- update account_group as ag 
-- set parent_id = ag2.id
-- from account_group ag2 
-- where ag2.name = left(ag.name, 2)
-- and length(ag.name) = 4;

-- update account_group as ag 
-- set parent_id = ag2.id
-- from account_group ag2 
-- where ag2.name = left(ag.name, 4)
-- and length(ag.name) = 6;

-- update account_group as ag 
-- set parent_id = ag2.id
-- from account_group ag2 
-- where ag2.name = left(ag.name, 6)
-- and length(ag.name) = 8;

-- update account_account as aa
-- set group_id = ag.id
-- from account_group ag 
-- where ag.name = left(aa.code, 4) 
-- and length(aa.code) = 6;

-- update account_account as aa
-- set group_id = ag.id
-- from account_group ag 
-- where ag.name = left(aa.code, 6) 
-- and length(aa.code) = 8;

-- update account_account as aa
-- set group_id = ag.id
-- from account_group ag 
-- where ag.name = left(aa.code, 8) 
-- and length(aa.code) = 10;

-- update account_group as ag 
-- set code_prefix_start = aa.min,
-- code_prefix_end = aa.max
-- from (select ag.id, lpad(cast(min(cast(right(aa.code, 2) as integer)) as character varying), 2, '0') as min, 
-- lpad(cast(max(cast(right(aa.code, 2) as integer)) as character varying), 2, '0') as max
-- from account_group ag 
-- inner join account_account aa on aa.group_id = ag.id 
-- group by ag.id) as aa 
-- where aa.id = ag.id;

-- insert into stock_valuation_layer (company_id, product_id, create_date, quantity, unit_cost, value, stock_move_id, description)
-- select sm.company_id,
-- sm.product_id,
-- sm.date,
-- sm.product_uom_qty,
-- sm.price_unit,
-- sm.price_unit * sm.product_uom_qty,
-- sm.id,
-- agofer.name
-- from stock_move sm 
-- inner join dblink('dbname=agofer_08','select sm.id,
-- sm.company_id,
-- sm.state,
-- pt.type,
-- sls.usage as sls_usage,
-- sls.company_id as sls_company_id,
-- sld.usage as sld_usage,
-- sld.company_id as sld_company_id,
-- sp.name 
-- from stock_move sm 
-- inner join product_product pp on pp.id = sm.product_id 
-- inner join product_template pt on pt.id = pp.product_tmpl_id 
-- inner join stock_location sls on sls.id = sm.location_id 
-- inner join stock_location sld on sld.id = sm.location_dest_id 
-- left join stock_picking sp on sp.id = sm.picking_id;') as agofer 
-- (id integer,
--  company_id integer,
--  state character varying, 
--  type character varying,
--  sls_usage character varying,
--  sls_company_id integer,
--  sld_usage character varying, 
--  sld_company_id integer,
--  name character varying) on sm.id = agofer.id
-- where agofer.state = 'done' 
-- and agofer.type = 'product' 
-- and not (agofer.sls_usage = 'internal' or (agofer.sls_usage = 'transit' and agofer.sls_company_id is not null))  
-- and (agofer.sld_usage = 'internal' or (agofer.sld_usage = 'transit' and agofer.sld_company_id is not null));

-- insert into stock_valuation_layer (company_id, product_id, create_date, quantity, unit_cost, value, stock_move_id, description)
-- select sm.company_id,
-- sm.product_id,
-- sm.date,
-- -sm.product_uom_qty,
-- sm.price_unit,
-- sm.price_unit * -sm.product_uom_qty,
-- sm.id,
-- agofer.name
-- from stock_move sm 
-- inner join dblink('dbname=agofer_08','select sm.id,
-- sm.company_id,
-- sm.state,
-- pt.type,
-- sls.usage as sls_usage,
-- sls.company_id as sls_company_id,
-- sld.usage as sld_usage,
-- sld.company_id as sld_company_id,
-- sp.name 
-- from stock_move sm 
-- inner join product_product pp on pp.id = sm.product_id 
-- inner join product_template pt on pt.id = pp.product_tmpl_id 
-- inner join stock_location sls on sls.id = sm.location_id 
-- inner join stock_location sld on sld.id = sm.location_dest_id 
-- left join stock_picking sp on sp.id = sm.picking_id;') as agofer 
-- (id integer,
--  company_id integer,
--  state character varying, 
--  type character varying,
--  sls_usage character varying,
--  sls_company_id integer,
--  sld_usage character varying, 
--  sld_company_id integer,
--  name character varying) on sm.id = agofer.id
-- where agofer.state = 'done' 
-- and agofer.type = 'product' 
-- and (agofer.sls_usage = 'internal' or (agofer.sls_usage = 'transit' and agofer.sls_company_id is not null))  
-- and not (agofer.sld_usage = 'internal' or (agofer.sld_usage = 'transit' and agofer.sld_company_id is not null));