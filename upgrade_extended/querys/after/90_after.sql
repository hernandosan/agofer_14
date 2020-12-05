insert into account_group (name, company_id, niif_bool) 
select left(code, -2), 1, False from account_account group by left(code, -2);

insert into account_group (name, company_id, niif_bool) 
select left(code, -4), 1, False from account_account group by left(code, -4);

insert into account_group (name, company_id, niif_bool) 
select left(code, -6), 1, False from account_account group by left(code, -6);

insert into account_group (name, company_id, niif_bool) 
select left(code, -8), 1, False from account_account group by left(code, -8);

insert into account_group (name, company_id, niif_bool) 
select left(code, -10), 1, False from account_account group by left(code, -10);

delete from account_group where name = '';

update account_group as ag 
set parent_id = ag2.id
from account_group ag2 
where ag2.name = left(ag.name, 2)
and length(ag.name) = 4;

update account_group as ag 
set parent_id = ag2.id
from account_group ag2 
where ag2.name = left(ag.name, 4)
and length(ag.name) = 6;

update account_group as ag 
set parent_id = ag2.id
from account_group ag2 
where ag2.name = left(ag.name, 6)
and length(ag.name) = 8;

update account_account as aa
set group_id = ag.id
from account_group ag 
where ag.name = left(aa.code, 4) 
and length(aa.code) = 6;

update account_account as aa
set group_id = ag.id
from account_group ag 
where ag.name = left(aa.code, 6) 
and length(aa.code) = 8;

update account_account as aa
set group_id = ag.id
from account_group ag 
where ag.name = left(aa.code, 8) 
and length(aa.code) = 10;

update account_group as ag 
set code_prefix_start = aa.min,
code_prefix_end = aa.max
from (select ag.id, lpad(cast(min(cast(right(aa.code, 2) as integer)) as character varying), 2, '0') as min, 
lpad(cast(max(cast(right(aa.code, 2) as integer)) as character varying), 2, '0') as max
from account_group ag 
inner join account_account aa on aa.group_id = ag.id 
group by ag.id) as aa 
where aa.id = ag.id;

update mail_alias ma 
set alias_name = agofer.alias_name
from dblink('dbname=agofer_08','SELECT id, alias_name FROM mail_alias;') as agofer (id integer, alias_name character varying)
where agofer.id = ma.id 
and ma.alias_name != agofer.alias_name;

update hr_job hj 
set alias_id = agofer.alias_id
from dblink('dbname=agofer_08','SELECT id, alias_id FROM hr_job;') as agofer (id integer, alias_id integer) 
inner join mail_alias ma on ma.id = agofer.alias_id
where agofer.id = hj.id and hj.alias_id != agofer.alias_id;

update hr_employee he 
set resource_id = agofer.resource_id
from dblink('dbname=agofer_08','SELECT id, resource_id FROM hr_employee;') as agofer (id integer, resource_id integer) 
inner join resource_resource rr on rr.id = agofer.resource_id
where agofer.id = he.id and he.resource_id != agofer.resource_id;

update ir_sequence ise 
set prefix = agofer.prefix,
suffix = agofer.suffix,
padding = agofer.padding,
number_next = agofer.number_next
from dblink('dbname=agofer_08','SELECT id, code, prefix, suffix, padding, number_next FROM ir_sequence;') as agofer 
(id integer, code character varying, prefix character varying, suffix character varying, padding integer, number_next integer) 
where agofer.id = ise.id;

update ir_sequence ise
set prefix = agofer.prefix,
suffix = agofer.suffix,
padding = agofer.padding,
number_next = agofer.number_next
from dblink('dbname=agofer_08','SELECT id, code, prefix, suffix, padding, number_next FROM ir_sequence;') as agofer
(id integer, code character varying, prefix character varying, suffix character varying, padding integer, number_next integer)
where agofer.code = ise.code;

update product_category set parent_path = '' where parent_path is null;

update product_category set parent_path = cast(id as character varying) || '/' where parent_path = '' and parent_id is null;

update stock_location set parent_path = '' where parent_path is null;

update stock_location set parent_path = cast(id as character varying) || '/' where parent_path = '' and location_id is null;

update account_account aa
set code = agofer.code
from dblink('dbname=agofer_08','SELECT id, code FROM account_account;') as agofer
(id integer, code character varying)
where agofer.id = aa.id;

update account_move_line aml
set statement_id = agofer.statement_id
from dblink('dbname=agofer_08','SELECT id, statement_id FROM account_move_line;') as agofer
(id integer, statement_id integer)
inner join account_bank_statement abs on agofer.statement_id = abs.id
where agofer.id = aml.id;

update account_move_line aml
set statement_line_id = agofer.statement_line_id
from dblink('dbname=agofer_08','SELECT id, statement_line_id FROM account_move_line;') as agofer
(id integer, statement_id integer)
inner join account_bank_statement_line abs on agofer.statement_line_id = abs.id
where agofer.id = aml.id;

update stock_picking as sp 
set sale_id = so.id
from procurement_group pg
inner join sale_order so on so.name = pg.name 
where pg.id = sp.group_id;

INSERT INTO stock_move_line (
	company_id, 
	product_id,
	product_uom_id, 
	product_uom_qty,
	move_id, 
	date,
	location_id,
	location_dest_id,
	state,
	product_qty,
	qty_done
)
SELECT 
	company_id, 
	product_id,
	product_uom,
	product_uom_qty,
	id ,
	date,
	location_id,
	location_dest_id,
	state,
	product_qty,
	product_qty
FROM stock_move 
WHERE state = done;

update stock_picking as sp 
set location_id = sm.location_id,
location_dest_id = sm.location_dest_id
from stock_move sm 
where sm.picking_id = sp.id;

update sale_order set pick_date = cast(date_order as date)
where shipping_type = 'pick' and pick_date is null;

update res_partner rp
set write_uid = agofer.write_uid,
create_uid = agofer.create_uid
from dblink('dbname=agofer_08','SELECT id, write_uid, create_uid FROM res_partner;') as agofer (id integer, write_uid integer, create_uid integer)
where agofer.id = rp.id;

update res_city as rc 
set state_id = rcs.id, country_id = rco.id
from dblink('dbname=agofer_08','select rc.id as id, rc.name as name, rcs.id as id2, rcs.name as name2, rco.code
from res_city rc 
inner join res_country_state rcs on rcs.id = rc.provincia_id
inner join res_country rco on rco.id = rcs.country_id 
order by rc.id, rcs.id;') as agofer (id integer, name character varying, id2 integer, name2 character varying, code character varying)
inner join res_country_state rcs on rcs.name = agofer.name2
inner join res_country rco on rco.code = agofer.code
where agofer.id = rc.id;

insert into stock_valuation_layer (company_id, product_id, create_date, quantity, unit_cost, value, stock_move_id, description)
select sm.company_id,
sm.product_id,
sm.date,
sm.product_uom_qty,
sm.price_unit,
sm.price_unit * sm.product_uom_qty,
sm.id,
agofer.name
from stock_move sm 
inner join dblink('dbname=agofer_08','select sm.id,
sm.company_id,
sm.state,
pt.type,
sls.usage as sls_usage,
sls.company_id as sls_company_id,
sld.usage as sld_usage,
sld.company_id as sld_company_id,
sp.name 
from stock_move sm 
inner join product_product pp on pp.id = sm.product_id 
inner join product_template pt on pt.id = pp.product_tmpl_id 
inner join stock_location sls on sls.id = sm.location_id 
inner join stock_location sld on sld.id = sm.location_dest_id 
left join stock_picking sp on sp.id = sm.picking_id;') as agofer 
(id integer,
 company_id integer,
 state character varying, 
 type character varying,
 sls_usage character varying,
 sls_company_id integer,
 sld_usage character varying, 
 sld_company_id integer,
 name character varying) on sm.id = agofer.id
where agofer.state = 'done' 
and agofer.type = 'product' 
and not (agofer.sls_usage = 'internal' or (agofer.sls_usage = 'transit' and agofer.sls_company_id is not null))  
and (agofer.sld_usage = 'internal' or (agofer.sld_usage = 'transit' and agofer.sld_company_id is not null));

insert into stock_valuation_layer (company_id, product_id, create_date, quantity, unit_cost, value, stock_move_id, description)
select sm.company_id,
sm.product_id,
sm.date,
-sm.product_uom_qty,
sm.price_unit,
sm.price_unit * -sm.product_uom_qty,
sm.id,
agofer.name
from stock_move sm 
inner join dblink('dbname=agofer_08','select sm.id,
sm.company_id,
sm.state,
pt.type,
sls.usage as sls_usage,
sls.company_id as sls_company_id,
sld.usage as sld_usage,
sld.company_id as sld_company_id,
sp.name 
from stock_move sm 
inner join product_product pp on pp.id = sm.product_id 
inner join product_template pt on pt.id = pp.product_tmpl_id 
inner join stock_location sls on sls.id = sm.location_id 
inner join stock_location sld on sld.id = sm.location_dest_id 
left join stock_picking sp on sp.id = sm.picking_id;') as agofer 
(id integer,
 company_id integer,
 state character varying, 
 type character varying,
 sls_usage character varying,
 sls_company_id integer,
 sld_usage character varying, 
 sld_company_id integer,
 name character varying) on sm.id = agofer.id
where agofer.state = 'done' 
and agofer.type = 'product' 
and (agofer.sls_usage = 'internal' or (agofer.sls_usage = 'transit' and agofer.sls_company_id is not null))  
and not (agofer.sld_usage = 'internal' or (agofer.sld_usage = 'transit' and agofer.sld_company_id is not null));

UPDATE resource_calendar 
SET create_uid = agofer.create_uid,
	create_date = agofer.create_date, 
	name = agofer.name,
	company_id = agofer.company_id,
	write_uid = agofer.write_uid,
	write_date = agofer.write_date, 
	tz = agofer.tz
FROM
	(select 
		agofer.id, 
		agofer.create_uid, 
		agofer.create_date, 
		agofer.name, 
		agofer.company_id, 
		agofer.write_uid, 
		agofer.write_date, 
		agofer.tz
		from dblink('dbname=agofer_08','SELECT 
			id, 
			create_uid, 
			create_date, 
			name, 
			company_id, 
			write_uid, 
			write_date, 
			tz
			FROM resource_calendar;'
		) as agofer(
			id integer, 
			create_uid integer, 
			create_date timestamp without time zone, 
			name character varying, 
			company_id integer, 
			write_uid integer, 
			write_date timestamp without time zone, 
			tz character varying
	))as agofer 
WHERE resource_calendar.id = agofer.id;