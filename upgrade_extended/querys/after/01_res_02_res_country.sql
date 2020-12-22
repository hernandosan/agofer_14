ALTER TABLE res_country DISABLE TRIGGER ALL;
DELETE FROM res_country;
ALTER TABLE res_country ENABLE TRIGGER ALL;

DELETE FROM ir_translation WHERE name = 'res.country,name';

INSERT INTO res_country (
    id,
    name,
    code,
    address_format,
    address_view_id,
    currency_id,
    phone_code,
    name_position,
    vat_label,
    state_required,
    zip_required,
    create_uid,
    create_date,
    write_uid,
    write_date,
    enforce_cities,
    street_format
) SELECT
    v8.id,
    v8.name,
    v8.code,
    v8.address_format,
    null,
    v8.currency_id,
    null,
    'before',
    null,
    false,
    true,
    2,
    v8.create_date,
    2,
    v8.write_date,
    false,
    '%(street)s'
from dblink('dbname=agofer_08','select
    id,
    substring(code,0,3),
    create_date,
    image,
    currency_id,
    write_date,
    name,
    address_format
    from res_country
    where id != 288;'
) AS v8 (
    id integer,
    code character varying,
    create_date timestamp without time zone,
    image bytea,
    currency_id integer,
    write_date timestamp without time zone,
    name character varying,
    address_format text
);

select setval('res_country_id_seq', (select max(id) from res_country));

--Se excluye id = 288 por unicidad de codigo
