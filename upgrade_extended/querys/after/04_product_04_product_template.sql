ALTER TABLE product_template DISABLE TRIGGER ALL;
DELETE FROM product_template;
ALTER TABLE product_template ENABLE TRIGGER ALL;

INSERT INTO product_template (
	id, 
    list_price,
    weight,
    color,
    write_uid,
    uom_id,
    description_purchase,
    create_date,
    create_uid,
    company_id,
    uom_po_id,
    type,
    description,
    volume,
    write_date,
    active,
    categ_id,
    sale_ok,
    name,
    description_sale,
    sale_delay,
    purchase_ok,
    produce_delay,
    sale_line_warn_msg,
    purchase_line_warn_msg,
    purchase_line_warn,
    sale_line_warn,
    landed_cost_ok,
    upload_delay,
	tracking
) SELECT
	agofer.id, 
	agofer.list_price, 
	agofer.weight, 
	agofer.color, 
	agofer.write_uid, 
	agofer.uom_id,
	agofer.description_purchase, 
	agofer.create_date, 
	agofer.create_uid, 
	agofer.company_id, 
	agofer.uom_po_id,
	agofer.type, 
	agofer.description, 
	agofer.volume, 
	agofer.write_date, 
	agofer.active, 
	agofer.categ_id, 
	agofer.sale_ok, 
	agofer.name, 
	agofer.description_sale, 
	agofer.sale_delay, 
	agofer.purchase_ok, 
	agofer.produce_delay, 
	agofer.sale_line_warn_msg, 
	agofer.purchase_line_warn_msg, 
	agofer.purchase_line_warn, 
	agofer.sale_line_warn, 
	agofer.landed_cost_ok,
	agofer.upload_delay,
	--agofer.tracking
	(CASE WHEN agofer.track_all = True THEN 'lot' ELSE 'none' END)
FROM dblink('dbname=agofer_08', 'select
	id, 
    list_price,
    weight,
    color,
    write_uid,
    uom_id,
    description_purchase,
    create_date,
    create_uid,
    company_id,
    uom_po_id,
    type,
    description,
    volume,
    write_date,
    active,
    categ_id,
    sale_ok,
    name,
    description_sale,
    sale_delay,
    purchase_ok,
    produce_delay,
    sale_line_warn_msg,
    purchase_line_warn_msg,
    purchase_line_warn,
    sale_line_warn,
    landed_cost_ok,
    upload_delay,
    track_all
	from product_template;'
) AS agofer(
	id integer, 
    list_price numeric,
    weight numeric,
    color integer,
    write_uid integer,
    uom_id integer,
    description_purchase text,
    create_date timestamp without time zone,
    create_uid integer,
    company_id integer,
    uom_po_id integer,
    type character varying,
    description text,
    volume double precision,
    write_date timestamp without time zone,
    active boolean,
    categ_id integer,
    sale_ok boolean,
    name character varying,
    description_sale text,
    sale_delay double precision,
    purchase_ok boolean,
    produce_delay double precision,
    sale_line_warn_msg text,
    purchase_line_warn_msg text,
    purchase_line_warn character varying,
    sale_line_warn character varying,
    landed_cost_ok boolean,
    upload_delay double precision,
    track_all boolean
);

select setval('product_template_id_seq', (select max(id) from product_template));