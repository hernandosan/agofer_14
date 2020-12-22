ALTER TABLE uom_category DISABLE TRIGGER ALL;
DELETE FROM uom_category;
ALTER TABLE uom_category ENABLE TRIGGER ALL;

INSERT INTO uom_category (
	id, 
	create_uid, 
	create_date, 
	name, 
	write_uid, 
	write_date
) SELECT
    agofer.id,
	agofer.create_uid, 
	agofer.create_date, 
	agofer.name, 
	agofer.write_uid, 
	agofer.write_date
FROM dblink('dbname=agofer_08', 'select
	id, 
	create_uid, 
	create_date, 
	name, 
	write_uid, 
	write_date
	from product_uom_categ;'
) AS agofer(
	id integer, 
	create_uid integer, 
	create_date timestamp without time zone, 
	name character varying, 
	write_uid integer, 
	write_date timestamp without time zone
);

select setval('uom_category_id_seq', (select max(id) from uom_category));