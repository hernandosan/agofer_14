ALTER TABLE resource_calendar DISABLE TRIGGER ALL;
DELETE FROM resource_calendar;
ALTER TABLE resource_calendar ENABLE TRIGGER ALL;

INSERT INTO resource_calendar (
	id,
    create_uid,
    create_date,
    name,
    company_id,
    write_uid,
    write_date,
    tz
) SELECT
	agofer.id,
    agofer.create_uid,
    agofer.create_date,
    agofer.name,
    agofer.company_id,
    agofer.write_uid,
    agofer.write_date,
    agofer.tz
FROM dblink('dbname=agofer_08','select
	id,
    create_uid,
    create_date,
    name,
    company_id,
    write_uid,
    write_date,
    tz
	from resource_calendar;'
) AS agofer(
	id integer, 
    create_uid integer,
    create_date timestamp without time zone,
    name character varying,
    company_id integer,
    write_uid integer,
    write_date timestamp without time zone,
    tz character varying
);

select setval('resource_calendar_id_seq', (select max(id) from resource_calendar));