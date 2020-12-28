ALTER TABLE resource_resource DISABLE TRIGGER ALL;
DELETE FROM resource_resource;
ALTER TABLE resource_resource ENABLE TRIGGER ALL;

INSERT INTO resource_resource (
	id,
	create_uid,
	time_efficiency,
	user_id,
	name,
	company_id,
	write_uid,
	create_date,
	write_date,
	active,
	calendar_id,
	resource_type,
	tz
) SELECT
	agofer.id,
	agofer.create_uid,
	agofer.time_efficiency,
	agofer.user_id,
	agofer.name,
	agofer.company_id,
	agofer.write_uid,
	agofer.create_date,
	agofer.write_date,
	agofer.active,
	agofer.calendar_id,
	agofer.resource_type,
	--agofer.tz
	'America/Bogota'
FROM dblink('dbname=agofer_08','select
	id,
	create_uid,
	time_efficiency,
	user_id,
	name,
	company_id,
	write_uid,
	create_date,
	write_date,
	active,
	calendar_id,
	resource_type
	from resource_resource;'
) AS agofer(
	id integer, 
	create_uid integer, 
	time_efficiency double precision, 
	user_id integer, 
	name character varying, 
	company_id integer, 
	write_uid integer, 
	create_date timestamp without time zone, 
	write_date timestamp without time zone, 
	active boolean, 
	calendar_id integer, 
	resource_type character varying
);

select setval('resource_resource_id_seq', (select max(id) from resource_resource));