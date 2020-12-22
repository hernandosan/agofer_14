ALTER TABLE product_category DISABLE TRIGGER ALL;
DELETE FROM product_category;
ALTER TABLE product_category ENABLE TRIGGER ALL;

INSERT INTO product_category (
	id, 
	create_uid, 
	create_date, 
	name, 
	write_uid, 
	parent_id, 
	write_date, 
	removal_strategy_id
) SELECT
    agofer.id,
	agofer.create_uid, 
	agofer.create_date, 
	agofer.name, 
	agofer.write_uid, 
	agofer.parent_id, 
	agofer.write_date, 
	agofer.removal_strategy_id 
FROM dblink('dbname=agofer_08','select
	id, 
	create_uid, 
	create_date, 
	name, 
	write_uid, 
	parent_id, 
	write_date, 
	removal_strategy_id
	from product_category;'
) AS agofer(
	id integer, 
	create_uid integer, 
	create_date timestamp without time zone, 
	name character varying, 
	write_uid integer, 
	parent_id integer, 
	write_date timestamp without time zone, 
	removal_strategy_id integer
);

select setval('product_category_id_seq', (select max(id) from product_category));