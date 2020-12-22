ALTER TABLE uom_uom DISABLE TRIGGER ALL;
DELETE FROM uom_uom;
ALTER TABLE uom_uom ENABLE TRIGGER ALL;

INSERT INTO uom_uom (
	id,
    create_date,
    write_uid,
    active,
    write_date,
    uom_type,
    create_uid,
    name,
    rounding,
    factor,
    category_id
) SELECT
	agofer.id,
    agofer.create_date,
    agofer.write_uid,
    agofer.active,
    agofer.write_date,
    agofer.uom_type,
    agofer.create_uid,
    agofer.name,
    agofer.rounding,
    agofer.factor,
    agofer.category_id
FROM dblink('dbname=agofer_08','SELECT
	id,
    create_date,
    write_uid,
    active,
    write_date,
    uom_type,
    create_uid,
    name,
    rounding,
    factor,
    category_id
	FROM product_uom;'
) AS agofer(
	id integer,
    create_date timestamp without time zone,
    write_uid integer,
    active boolean,
    write_date timestamp without time zone,
    uom_type character varying,
    create_uid integer,
    name character varying,
    rounding numeric,
    factor numeric,
    category_id integer
);

select setval('uom_uom_id_seq', (select max(id) from uom_uom));