INSERT INTO stock_valuation_layer (
    company_id,
    product_id,
    create_date,
    quantity,
    unit_cost,
    value,
    stock_move_id,
    description
) SELECT
    sm.company_id,
    sm.product_id,
    sm.date,
    sm.product_uom_qty,
    sm.price_unit,
    sm.price_unit * sm.product_uom_qty,
    sm.id,
    agofer.name
    from stock_move sm
INNER JOIN dblink('dbname=agofer_08','select
    sm.id,
    sm.company_id,
    sm.state,
    pt.type,
    sls.usage as sls_usage,
    sls.company_id as sls_company_id,
    sld.usage as sld_usage,
    sld.company_id as sld_company_id,
    sp.name
    FROM stock_move sm
INNER JOIN product_product pp ON pp.id = sm.product_id
INNER JOIN product_template pt ON pt.id = pp.product_tmpl_id
INNER JOIN stock_location sls ON sls.id = sm.location_id
INNER JOIN stock_location sld ON sld.id = sm.location_dest_id
LEFT JOIN stock_picking sp ON sp.id = sm.picking_id;'
) AS agofer (
    id integer,
    company_id integer,
    state character varying,
    type character varying,
    sls_usage character varying,
    sls_company_id integer,
    sld_usage character varying,
    sld_company_id integer,
    name character varying
) ON sm.id = agofer.id
WHERE agofer.state = 'done'
AND agofer.type = 'product'
AND NOT (agofer.sls_usage = 'internal' OR (agofer.sls_usage = 'transit' AND agofer.sls_company_id IS NOT NULL))
AND (agofer.sld_usage = 'internal' OR (agofer.sld_usage = 'transit' AND agofer.sld_company_id IS NOT NULL));



select setval('stock_quant_id_seq', (select max(id) from stock_quant));