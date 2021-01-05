ALTER TABLE res_currency DISABLE TRIGGER ALL;
DELETE FROM res_currency;
ALTER TABLE res_currency ENABLE TRIGGER ALL;

INSERT INTO res_currency (
    id,
    name,
    symbol,
    rounding,
    decimal_places,
    active,
    position,
    currency_unit_label,
    currency_subunit_label,
    create_uid,
    create_date,
    write_uid,
    write_date
) SELECT
    v8.id,
    v8.name,
    COALESCE(v8.symbol,'$'),
    v8.rounding,
    v8.accuracy,
    v8.active,
    v8.position,
    (CASE WHEN v8.name = 'COP' THEN 'PESO' WHEN v8.name = 'EUR' THEN 'Euros' WHEN v8.name = 'USD' THEN 'Dollars' END),
    (CASE WHEN v8.name = 'COP' THEN 'Centavos' WHEN v8.name = 'EUR' THEN 'Cents' WHEN v8.name = 'USD' THEN 'Cents' END),
    2,
    v8.create_date,
    2,
    v8.write_date
from dblink('dbname=agofer_08',' select
    id,
    name,
    create_uid,
    create_date,
    rounding,symbol,
    company_id,
    write_uid,
    base,
    write_date,
    active,
    position,
    accuracy,
    rounding_invoice,
    name_print
    from res_currency;'
) AS v8 (
    id integer,
    name character varying,
    create_uid integer,
    create_date timestamp without time zone,
    rounding numeric,
    symbol character varying(4),
    company_id integer,
    write_uid integer,
    base boolean,
    write_date timestamp without time zone,
    active boolean,
    position character varying,
    accuracy integer,
    rounding_invoice integer,
    name_print character varying
);

select setval('res_currency_id_seq', (select max(id) from res_currency));