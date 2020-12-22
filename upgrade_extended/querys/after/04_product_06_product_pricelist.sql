ALTER TABLE product_pricelist DISABLE TRIGGER ALL;
DELETE FROM product_pricelist;
ALTER TABLE product_pricelist ENABLE TRIGGER ALL;

INSERT INTO product_pricelist (
	id, 
	create_date, 
	write_uid, 
	currency_id, 
	write_date, 
	active, 
	create_uid, 
	name, 
	company_id,
	discount_policy
) SELECT
	agofer.id, 
	agofer.create_date, 
	agofer.write_uid, 
	agofer.currency_id,
	agofer.write_date, 
	agofer.active, 
	agofer.create_uid, 
	agofer.name, 
	agofer.company_id,
	--agofer.discount_policy
	'with_discount'
FROM dblink('dbname=agofer_08', 'select
	id, 
	create_date, 
	write_uid, 
	currency_id, 
	write_date, 
	active, 
	create_uid, 
	name, 
	company_id
	from product_pricelist;'
) AS agofer (
	id integer, 
	create_date timestamp without time zone, 
	write_uid integer, 
	currency_id integer, 
	write_date timestamp without time zone, 
	active boolean, 
	create_uid integer, 
	name character varying, 
	company_id integer
);

select setval('product_pricelist_id_seq', (select max(id) from product_pricelist));