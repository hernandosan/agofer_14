ALTER TABLE mail_followers DISABLE TRIGGER ALL;
DELETE FROM mail_followers;
ALTER TABLE mail_followers ENABLE TRIGGER ALL;

INSERT INTO mail_followers (
    id,
	res_model,
	res_id,
	partner_id
) SELECT
    agofer.id,
	agofer.res_model,
	agofer.res_id,
	agofer.partner_id
FROM dblink('dbname=agofer_08','select
    id,
	res_model,
	res_id,
	partner_id
    FROM mail_followers;'
) AS agofer (
    id integer,
	res_model character varying,
	res_id integer,
	partner_id integer
)INNER JOIN ir_model IR ON IR.model = agofer.res_model;

select setval('mail_followers_id_seq', (select max(id) from mail_followers));