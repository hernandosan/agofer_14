INSERT INTO hr_leave_cause (
	id,
	name,
	code,
	create_uid,
	create_date,
	write_uid,
	write_date
) SELECT
	agofer.id,
	agofer.name,
	agofer.code,
	agofer.create_uid,
	agofer.create_date,
	agofer.write_uid,
	agofer.write_date
FROM dblink('dbname=agofer_08', 'SELECT
	tipo.id as id,
	tipo.name as name,
	tipo.code as code,
	tipo.create_uid as create_uid,
	tipo.create_date as create_date,
	tipo.write_uid as write_uid,
	tipo.write_date as write_date
    FROM hr_holidays_status_incapacity AS tipo'
) AS agofer (
	id integer,
	name character varying,
	code character varying,
	create_uid integer,
	create_date timestamp without time zone,
	write_uid integer,
	write_date timestamp without time zone
)
WHERE agofer.id NOT IN (SELECT id FROM hr_leave_cause);

select setval('hr_leave_cause_id_seq', (select max(id) from hr_leave_cause));