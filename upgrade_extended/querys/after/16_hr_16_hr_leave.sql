INSERT INTO hr_leave (
	id,
	name,
	contract_id,
	leave_type_id,
	approve_date,
	date_start,
	date_end,
	state,
	days_vac_money,
	number_order_eps,
	cause_id,
	company_id,
	create_uid,
	create_date,
	write_uid,
	write_date
) SELECT
	agofer.id,
	agofer.name,
	--agofer.contract_id,
	3,
	agofer.holiday_status_id,
	agofer.approve_date,
	agofer.date_from,
	agofer.date_to,
	agofer.state,
	agofer.payed_vac,
	agofer.no_incapacidad,
	agofer.incapacity,
	--agofer.company_id
	1,
	agofer.create_uid,
	agofer.create_date,
	agofer.write_uid,
	agofer.write_date
FROM dblink('dbname=agofer_08', 'SELECT
	ausencia.id AS id,
	ausencia.name AS name,
	ausencia.contract_id AS contract_id,
	ausencia.holiday_status_id AS holiday_status_id,
	ausencia.approve_date AS approve_date,
	ausencia.date_from AS date_from,
	ausencia.date_to AS date_to,
	ausencia.state AS state,
	ausencia.payed_vac AS payed_vac,
	ausencia.no_incapacidad AS no_incapacidad,
	ausencia.incapacity AS incapacity,
	ausencia.create_uid AS create_uid,
	ausencia.create_date AS create_date,
	ausencia.write_uid AS write_uid,
	ausencia.write_date AS write_date
FROM
	hr_holidays AS ausencia
WHERE contract_id IS NOT NULL'
) AS agofer(
	id integer,
	name character varying,
	contract_id integer,
	holiday_status_id integer,
	approve_date timestamp without time zone,
	date_from timestamp without time zone,
	date_to timestamp without time zone,
	state character varying,
	payed_vac numeric,
	no_incapacidad character varying,
	incapacity integer,
	create_uid integer,
	create_date timestamp without time zone,
	write_uid integer,
	write_date timestamp without time zone
)
WHERE agofer.id NOT IN (SELECT id FROM hr_leave);

select setval('hr_leave_id_seq', (select max(id) from hr_leave));