INSERT INTO helpdesk_ticket_category (
	id,
	active,
	name,
	create_uid,
	create_date,
	write_uid,
	write_date,
	team_id,
	company_id
) SELECT
	agofer.id,
	agofer.active,
	agofer.name,
	agofer.create_uid,
	agofer.create_date,
	agofer.write_uid,
	agofer.write_date,
	agofer.category_id,
	--agofer.company_id
	1
FROM dblink('dbname=agofer_08','select
	id,
	active,
	name,
	create_uid,
	create_date,
	write_uid,
	write_date,
	category_id
	from website_support_ticket_platforms;'
) AS agofer(
	id integer,
	active boolean,
	name character varying,
	create_uid integer,
	create_date timestamp without time zone,
	write_uid integer,
	write_date timestamp without time zone,
	category_id integer
);

select setval('helpdesk_ticket_category_id_seq', (select max(id) from helpdesk_ticket_category));