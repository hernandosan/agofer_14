INSERT INTO helpdesk_ticket_team (
	id,
	create_uid,
	create_date,
	name,
	write_uid,
	write_date,
	active,
	company_id,
	alias_id
) SELECT
	agofer.id,
	agofer.create_uid,
	agofer.create_date,
	agofer.name,
	agofer.write_uid,
	agofer.write_date,
	--agofer.active
	'True',
	--agofer.company_id
	1,
	--agofer.alias_id
	1
FROM dblink('dbname=agofer_08','SELECT
	id,
	create_uid,
	create_date,
	name,
	write_uid,
	write_date
	FROM website_support_ticket_categories;'
) AS agofer(
	id integer, 
	create_uid integer, 
	create_date timestamp without time zone, 
	name character varying, 
	write_uid integer, 
	write_date timestamp without time zone
);

select setval('helpdesk_ticket_team_id_seq', (select max(id) from helpdesk_ticket_team));