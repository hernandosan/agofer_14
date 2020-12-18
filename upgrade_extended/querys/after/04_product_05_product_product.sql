INSERT INTO product_product (
    id,
    create_uid,
    create_date,
    write_uid,
    default_code,
    write_date,
    active,
    product_tmpl_id,
    barcode
) SELECT
    agofer.id,
    agofer.create_uid,
    agofer.create_date,
    agofer.write_uid,
    agofer.default_code,
    agofer.write_date,
    agofer.active,
    agofer.product_tmpl_id,
    agofer.ean13
FROM dblink('dbname=agofer_08', 'select
    id,
    create_uid,
    create_date,
    write_uid,
    default_code,
    write_date,
    active,
    product_tmpl_id,
    ean13
    from product_product;'
) AS agofer (
    id integer,
    create_uid integer,
    create_date timestamp without time zone,
    write_uid integer,
    default_code character varying,
    write_date timestamp without time zone,
    active boolean,
    product_tmpl_id integer
    ean13 character varying
)
WHERE agofer.id NOT IN (SELECT id FROM product_product);

select setval('product_product_id_seq', (select max(id) from product_product));

update product_product as pp 
set weight = pt.weight
from product_template pt
where pt.id = pp.product_tmpl_id;