ALTER TABLE res_partner_title DISABLE TRIGGER ALL;
DELETE FROM res_partner_title;
ALTER TABLE res_partner_title ENABLE TRIGGER ALL;

INSERT INTO res_partner_title (
	id,
    create_uid,
    create_date,
    name,
    shortcut,
    write_uid,
    write_date
) SELECT
    agofer.id,
    --agofer.create_uid,
    2,
    agofer.create_date,
    agofer.name,
    agofer.shortcut,
    --agofer.write_uid,
    2,
    agofer.write_date
FROM dblink('dbname=agofer_08', 'select
	id,
    create_uid,
    create_date,
    name,
    shortcut,
    write_uid,
    write_date
	FROM res_partner_title;'
) AS agofer(
	id integer,
    create_uid integer,
    create_date timestamp without time zone,
    name character varying,
    shortcut character varying,
    write_uid integer,
    write_date timestamp without time zone
);

select setval('res_partner_title_id_seq', (select max(id) from res_partner_title));