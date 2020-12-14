insert into hr_job (
	id, 
	create_date, 
	description, 
	write_uid, 
	write_date, 
	create_uid, 
	no_of_hired_employee, 
	requirements, 
	name, 
	company_id, 
	state, 
	no_of_recruitment, 
	expected_employees, 
	no_of_employee, 
	department_id, 
	address_id, 
	color, 
	alias_id, 
	user_id, 
	manager_id
) select 
	agofer.id, 
	agofer.create_date, 
	agofer.description, 
	agofer.write_uid, 
	agofer.write_date, 
	agofer.create_uid, 
	agofer.no_of_hired_employee, 
	agofer.requirements, 
	agofer.name, 
	agofer.company_id, 
	agofer.state, 
	agofer.no_of_recruitment, 
	agofer.expected_employees, 
	agofer.no_of_employee, 
	agofer.department_id, 
	agofer.address_id, 
	agofer.color, 
	--agofer.alias_id,
	1,
	agofer.user_id, 
	--agofer.manager_id
	1
from dblink('dbname=agofer_08','SELECT 
	id, 
	create_date, 
	description, 
	write_uid, 
	write_date, 
	create_uid, 
	no_of_hired_employee, 
	requirements, 
	name, 
	company_id, 
	state, 
	no_of_recruitment, 
	expected_employees, 
	no_of_employee, 
	department_id, 
	address_id, 
	color, 
	alias_id, 
	user_id, 
	manager_id
	FROM hr_job;'
) as agofer(
	id integer, 
	create_date timestamp without time zone, 
	description text, 
	write_uid integer, 
	write_date timestamp without time zone, 
	create_uid integer, 
	no_of_hired_employee integer, 
	requirements text, 
	name character varying, 
	company_id integer, 
	state character varying, 
	no_of_recruitment integer, 
	expected_employees integer, 
	no_of_employee integer, 
	department_id integer, 
	address_id integer, 
	color integer, 
	alias_id integer, 
	user_id integer, 
	manager_id integer
);

select setval('hr_job_id_seq', (select max(id) from hr_job));

update hr_job hj 
set alias_id = agofer.alias_id
from dblink('dbname=agofer_08','SELECT id, alias_id FROM hr_job;') as agofer (id integer, alias_id integer) 
inner join mail_alias ma on ma.id = agofer.alias_id
where agofer.id = hj.id and hj.alias_id != agofer.alias_id;