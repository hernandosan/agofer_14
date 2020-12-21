ALTER TABLE res_country_state DISABLE TRIGGER ALL;
DELETE FROM res_country_state;
ALTER TABLE res_country_state ENABLE TRIGGER ALL;

INSERT INTO res_country_state (
    id,
    country_id,
    name,
    code,
    create_uid,
    create_date,
    write_uid,
    write_date
) SELECT
    v8.id,
    v8.country_id,
    v8.name,
    v8.code,
    2,
    v8.create_date,
    2,
    v8.write_date
FROM dblink('dbname=agofer_08','select
    id,
    country_id,
    name,
    code,
    create_date,
    write_date
    from res_country_state
    where country_id != 288;'
) AS v8 (
    id integer,
    country_id integer,
    name character varying,
    code character varying,
    create_date timestamp without time zone,
    write_date timestamp without time zone
);

select setval('res_country_state_id_seq', (select max(id) from res_country_state));