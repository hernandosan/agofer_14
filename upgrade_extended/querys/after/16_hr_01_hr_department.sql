ALTER TABLE hr_department DISABLE TRIGGER ALL;
DELETE FROM hr_department;
ALTER TABLE hr_department ENABLE TRIGGER ALL;

INSERT INTO hr_department (
	id, 
	create_uid, 
	create_date, 
	name, 
	company_id, 
	write_uid, 
	note, 
	parent_id, 
	manager_id, 
	write_date,
	active
) SELECT
	agofer.id, 
	agofer.create_uid, 
	agofer.create_date, 
	agofer.name, 
	agofer.company_id, 
	agofer.write_uid, 
	agofer.note, 
	agofer.parent_id, 
	--agofer.manager_id,
	1,
	agofer.write_date,
	--agofer.active
	TRUE
FROM dblink('dbname=agofer_08','select
	id, 
	create_uid, 
	create_date, 
	name, 
	company_id, 
	write_uid, 
	note, 
	parent_id, 
	manager_id, 
	write_date
	from hr_department;'
) AS agofer (
	id integer, 
	create_uid integer, 
	create_date timestamp without time zone, 
	name character varying, 
	company_id integer, 
	write_uid integer, 
	note text, 
	parent_id integer, 
	manager_id integer, 
	write_date timestamp without time zone
);

select setval('hr_department_id_seq', (select max(id) from hr_department));