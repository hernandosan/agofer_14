INSERT INTO mrp_workcenter (
	id,
    create_uid,
    time_start,
    product_id,
    resource_id,
    time_stop,
    note,
    costs_hour,
    costs_hour_account_id,
    write_date,
    create_date,
    write_uid,
    active,
    company_id
) SELECT
    agofer.id,
    agofer.create_uid,
    agofer.time_start,
    agofer.product_id,
    agofer.resource_id,
    agofer.time_stop,
    agofer.note,
    agofer.costs_hour,
    agofer.costs_hour_account_id,
    agofer.write_date,
    agofer.create_date,
    agofer.write_uid,
    --agofer.active,
    TRUE,
    --agofer.company_id
    1
FROM dblink('dbname=agofer_08', 'select
	id,
    create_uid,
    time_start,
    product_id,
    resource_id,
    time_stop,
    note,
    costs_hour,
    costs_hour_account_id,
    write_date,
    create_date,
    write_uid
	from mrp_production;'
) AS agofer (
	id integer,
    create_uid integer,
    time_start double precision,
    product_id integer,
    resource_id integer,
    time_stop double precision,
    note text,
    costs_hour double precision,
    costs_hour_account_id integer,
    write_date timestamp without time zone,
    create_date timestamp without time zone,
    write_uid integer
);

SELECT setval('mrp_production_id_seq', (SELECT max(id) FROM mrp_production));
