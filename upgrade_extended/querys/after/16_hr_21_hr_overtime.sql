INSERT INTO hr_overtime (
	id,
	name,
	payslip_id,
	contract_id,
	overtime_type_id,
	approve_date,
	date_start,
	date_end,
	qty,
	state,
	company_id,
	create_uid,
	create_date,
	write_uid,
	write_date
) SELECT
	agofer.id,
	agofer.name,
	-- agofer.payslip_id,
	2,
	-- agofer.contract_id,
	3,
	agofer.type_id,
	agofer.approve_date,
	agofer.date_start,
	agofer.date_end,
	agofer.duracion,
	agofer.state,
	--agofer.company_id
	1,
	agofer.create_uid,
	agofer.create_date,
	agofer.write_uid,
	agofer.write_date
FROM dblink('dbname=agofer_08', 'select
	id,
	name,
	payslip_id,
	contract_id,
	type_id,
	approve_date,
	date_start,
	date_end,
	duracion,
	state,
	create_uid,
	create_date,
	write_uid,
	write_date
    from hr_payroll_extrahours;'
) AS agofer(
	id integer,
	name character varying,
	payslip_id integer,
	contract_id integer,
	type_id integer,
	approve_date date,
	date_start date,
	date_end date,
	duracion double precision,
	state character varying,
	create_uid integer,
	create_date timestamp without time zone,
	write_uid integer,
	write_date timestamp without time zone
)
WHERE agofer.id NOT IN (SELECT id FROM hr_overtime);

select setval('hr_overtime_id_seq', (select max(id) from hr_overtime));
