--Update res_city
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

--Update res_partner
update res_partner as rp
set state_id = rcs.id, country_id = rcc.id
from dblink('dbname=agofer_08','select rp.id, rc.name as rc_name, rcs.name as rcs_name, rcc.code as rcc_code
from res_partner rp
left join res_city rc on rc.id = rp.city_id
left join res_country_state rcs on rcs.id = rp.state_id
left join res_country rcc on rcc.id = rp.country_id;'
) as agofer (id integer, rc_name character varying, rcs_name character varying, rcc_code character varying)
inner join res_country_state rcs on rcs.name = agofer.rcs_name
inner join res_country rcc on rcc.code = agofer.rcc_code
where agofer.id = rp.id;

update res_partner rp
set write_uid = agofer.write_uid,
create_uid = agofer.create_uid
from dblink('dbname=agofer_08','SELECT id, write_uid, create_uid FROM res_partner;') as agofer (id integer, write_uid integer, create_uid integer)
where agofer.id = rp.id;

update res_partner set credit_control = True, credit_type = 'insured' where credit_limit > 0 and parent_id is null;

--Update res_users
update res_users set active = False where login not like '%agofer%' and login != 'admin';

--Update res_bank
UPDATE res_bank rb
	set name = agofer.name, street = agofer.street, street2 = agofer.street2, zip = agofer.zip, city = agofer.city, state = agofer.state, country = agofer.country,
	email = agofer.email, phone = agofer.phone, active = agofer.active,	bic = agofer.bic, create_uid = agofer.create_uid, create_date = agofer.create_date,
	write_uid = agofer.write_uid, write_date = agofer.write_date
FROM dblink('dbname=agofer_08','SELECT
	id,	name, street, street2, zip, city, state, country, email, phone,	active,	bic, create_uid, create_date, write_uid, write_date	from res_bank where id = 1;'
) AS agofer (
	id integer,	name character varying,	street character varying, street2 character varying, zip character varying,	city character varying,	state integer,
	country integer, email character varying, phone character varying, active boolean, bic character varying, create_uid integer, create_date timestamp without time zone,
	write_uid integer, write_date timestamp without time zone
)
WHERE agofer.id = rb.id;

--Update ir_sequence
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

--Update mail_message_type
UPDATE mail_message_subtype mms
SET parent_id = agofer.parent_id
from dblink('dbname=agofer_08','SELECT id, parent_id FROM mail_message_subtype where id>27;') as agofer
(id integer, parent_id integer)
where agofer.id = mms.id;

--Update mail_alias
update mail_alias ma
set alias_name = agofer.alias_name
from dblink('dbname=agofer_08','SELECT id, alias_name FROM mail_alias;') as agofer (id integer, alias_name character varying)
where agofer.id = ma.id
and ma.alias_name != agofer.alias_name;

--Update product_category
UPDATE product_category pc
SET name = agofer.name, complete_name = null
from dblink('dbname=agofer_08','SELECT id, name FROM product_category where id=4;') as agofer
(id integer, name character varying)
where agofer.id = pc.id;
where agofer.id = pc.id;

update product_category set parent_path = '' where parent_path is null;

update product_category set parent_path = cast(id as character varying) || '/' where parent_path = '' and parent_id is null;

--Update product_template
UPDATE product_template SET uom_id = 24 WHERE uom_id = 28;

UPDATE product_template SET uom_id = 23 WHERE uom_id = 20;

UPDATE product_template SET uom_id = 20 WHERE uom_id = 19;

UPDATE product_template SET uom_id = 20 WHERE uom_id = 42;

UPDATE product_template SET uom_id = 25 WHERE uom_id = 29;

UPDATE product_template SET uom_id = 19 WHERE uom_id = 18;

UPDATE product_template SET uom_id = 16 WHERE uom_id = 15;

--Update product_pricelist
update product_pricelist set currency_id = 2 where currency_id = 3;

update product_pricelist set currency_id = 8 where currency_id = 9;

--Update account_payment_term
update account_payment_term set company_id = 1;

--Update account_journal
update account_journal set currency_id = 2 where currency_id = 3;

update account_journal set currency_id = 8 where currency_id = 9;

--Update account_account
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

update account_group as ag
set code_prefix_start = aa.min,
code_prefix_end = aa.max
from (select ag.id, lpad(cast(min(cast(right(aa.code, 2) as integer)) as character varying), 2, '0') as min,
lpad(cast(max(cast(right(aa.code, 2) as integer)) as character varying), 2, '0') as max
from account_group ag
inner join account_account aa on aa.group_id = ag.id
group by ag.id) as aa
where aa.id = ag.id;

delete from account_group where name = '';

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

update account_account aa
set code = agofer.code
from dblink('dbname=agofer_08','SELECT id, code FROM account_account;')
as agofer (id integer, code character varying)
where agofer.id = aa.id;

--Update account_bank_statement
update account_bank_statement abs
set journal_id = agofer.journal_id
from dblink('dbname=agofer_08','SELECT id, journal_id FROM account_bank_statement;')
as agofer (id integer, journal_id integer)
where agofer.id = abs.id;

--Update account_move_line
update account_move_line aml
set statement_id = agofer.statement_id, statement_line_id = agofer.statement_line_id
from dblink('dbname=agofer_08','SELECT id, statement_id, statement_line_id FROM account_move_line;')
as agofer (id integer, statement_id integer, statement_line_id integer)
where agofer.id = aml.id;

--Update account_asset_profile

--Update stock_location
update stock_location set parent_path = '' where parent_path is null;

update stock_location set parent_path = cast(id as character varying) || '/' where parent_path = '';

--Update stock_picking_type
update stock_picking_type spt
set warehouse_id = agofer.warehouse_id
from dblink('dbname=agofer_08','SELECT id, warehouse_id FROM stock_picking_type;')
as agofer (id integer, warehouse_id integer)
where agofer.id = spt.id;

--Update stock_rule
update stock_rule sr
set warehouse_id = agofer.warehouse_id
from dblink('dbname=agofer_08','SELECT id, warehouse_id FROM procurement_rule;')
as agofer (id integer, warehouse_id integer)
where agofer.id = sr.id;

--Update stock_picking
update stock_picking as sp
set order_id = so.id
from procurement_group pg
inner join sale_order so on so.name = pg.name
where pg.id = sp.group_id;

update stock_picking as sp
set location_id = sm.location_id,
location_dest_id = sm.location_dest_id
from stock_move sm
where sm.picking_id = sp.id;

update stock_picking set scheduled_date = date where scheduled_date is null;

update stock_picking set shipping_type = null where order_id is null;

update stock_picking as sp
set shipping_type = null
from stock_picking_type spt
where spt.id = sp.picking_type_id
and spt.code != 'outgoing'
and sp.shipping_type is not null;

update stock_picking set delivery_bool = True where shipping_type = 'delivery' and delivery_date is null;

update stock_picking set delivery_bool = True where shipping_type = 'pick' and pick_date is null;

-- Update hr_job
update hr_job hj
set alias_id = agofer.alias_id
from dblink('dbname=agofer_08','SELECT id, alias_id FROM hr_job;') as agofer (id integer, alias_id integer)
inner join mail_alias ma on ma.id = agofer.alias_id
where agofer.id = hj.id and hj.alias_id != agofer.alias_id;

--Update hr_employee
update hr_employee he
set resource_id = agofer.resource_id
from dblink('dbname=agofer_08','SELECT id, resource_id FROM hr_employee;') as agofer (id integer, resource_id integer)
inner join resource_resource rr on rr.id = agofer.resource_id
where agofer.id = he.id and he.resource_id != agofer.resource_id;

update hr_employee as he
set active = True
from hr_contract hc
where hc.employee_id = he.id
and hc.date_end is null;

--Update stock_move_line
update stock_move_line sml
set move_id = agofer.move_id
from dblink('dbname=agofer_08','select spo.id, sm.id as move_id
from stock_pack_operation spo
inner join stock_move sm on sm.picking_id = spo.picking_id and sm.product_id = spo.product_id;') as agofer (id integer, move_id integer)
inner join stock_move sm on sm.id = agofer.move_id
where agofer.id = sml.id;

--Update sale_order
update sale_order set pick_date = cast(date_order as date)
where shipping_type = 'pick' and pick_date is null;

update sale_order as so
set team_id = rp.team_id
from res_partner rp
where rp.id = so.partner_id
and so.team_id is null
and rp.team_id is not null;

--Update ir_property
insert into ir_property (name, res_id, company_id, fields_id, value_text, type)
select 'property_cost_method',
'product.category,' || cast(pc.id as character varying),
1,
8419,
'average',
'selection'
from product_product pp
inner join product_template pt on pt.id = pp.product_tmpl_id
inner join product_category pc on pc.id = pt.categ_id
where pt.type = 'product'
and pp.active = True
group by pc.id
order by pc.id;

insert into ir_property (name, res_id, company_id, fields_id, value_text, type)
select 'property_valuation',
'product.category,' || cast(pc.id as character varying),
1,
8418,
'real_time',
'selection'
from product_product pp
inner join product_template pt on pt.id = pp.product_tmpl_id
inner join product_category pc on pc.id = pt.categ_id
where pt.type = 'product'
and pp.active = True
group by pc.id
order by pc.id;



update product_product as pp
set weight = pt.weight
from product_template pt
where pt.id = pp.product_tmpl_id;
