insert into hr_contract (
	id, 
	date_end, 
	write_uid, 
	write_date, 
	trial_date_end, 
	create_date, 
	job_id, 
	wage, 
	create_uid, 
	employee_id, 
	name, 
	notes, 
	date_start, 
	company_id, 
	state,
	active,
	schedule_pay
) select 
	agofer.id, 
	agofer.date_end, 
	agofer.write_uid, 
	agofer.write_date, 
	agofer.trial_date_end, 
	agofer.create_date, 
	agofer.job_id, 
	agofer.wage, 
	agofer.create_uid, 
	agofer.employee_id, 
	agofer.name, 
	agofer.notes, 
	agofer.date_start, 
	agofer.company_id, 
	agofer.state,
	--agofer.active
	TRUE,
	--agofer.schedule_pay
    'MONTHLY'
from dblink('dbname=agofer_08','SELECT 
	id, 
	date_end, 
	write_uid, 
	write_date, 
	trial_date_end, 
	create_date, 
	job_id, 
	wage, 
	create_uid, 
	employee_id, 
	name, 
	notes, 
	date_start, 
	company_id, 
	state
	FROM hr_contract;'
) as agofer(
	id integer, 
	date_end date, 
	write_uid integer, 
	write_date timestamp without time zone, 
	trial_date_end date, 
	create_date timestamp without time zone, 
	job_id integer, 
	wage numeric, 
	create_uid integer, 
	employee_id integer, 
	name character varying, 
	notes text, 
	date_start date, 
	company_id integer, 
	state character varying
);

select setval('hr_contract_id_seq', (select max(id) from hr_contract));