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