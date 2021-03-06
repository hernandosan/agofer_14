INSERT INTO procurement_group (
    id,
    create_uid,
    create_date,
    name,
    move_type,
    write_uid,
    write_date,
    partner_id
) SELECT
    agofer.id,
    agofer.create_uid,
    agofer.create_date,
    agofer.name,
    agofer.move_type,
    agofer.write_uid,
    agofer.write_date,
    agofer.partner_id
from dblink('dbname=agofer_08', 'select
    id,
    create_uid,
    create_date,
    name,
    move_type,
    write_uid,
    write_date,
    partner_id
    from procurement_group;'
) AS agofer (
    id integer,
    create_uid integer,
    create_date timestamp without time zone,
    name character varying,
    move_type character varying,
    write_uid integer,
    write_date timestamp without time zone,
    partner_id integer
);

select setval('procurement_group_id_seq', (select max(id) from procurement_group));