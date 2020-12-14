insert into product_category (
	id, 
	create_uid, 
	create_date, 
	name, 
	write_uid, 
	parent_id, 
	write_date, 
	removal_strategy_id)
	select agofer.id, 
	agofer.create_uid, 
	agofer.create_date, 
	agofer.name, 
	agofer.write_uid, 
	agofer.parent_id, 
	agofer.write_date, 
	agofer.removal_strategy_id 
from dblink('dbname=agofer_08','select 
	id, 
	create_uid, 
	create_date, 
	name, 
	write_uid, 
	parent_id, 
	write_date, 
	removal_strategy_id
	from product_category;'
) as agofer(
	id integer, 
	create_uid integer, 
	create_date timestamp without time zone, 
	name character varying, 
	write_uid integer, 
	parent_id integer, 
	write_date timestamp without time zone, 
	removal_strategy_id integer
)where agofer.id not in (select id from product_category);

select setval('product_category_id_seq', (select max(id) from product_category));

update product_category set parent_path = '' where parent_path is null;

update product_category set parent_path = cast(id as character varying) || '/' where parent_path = '' and parent_id is null;

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