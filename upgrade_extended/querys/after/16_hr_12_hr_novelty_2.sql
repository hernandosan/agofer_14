INSERT INTO hr_novelty (
	name,
	type_novelty,
	novelty_type_id,
	state,
	contract_id,
	approve_date,
	date_start,
	date_end,
	amount,
	company_id,
	create_uid,
	create_date,
	write_uid,
	write_date
)SELECT
	agofer.name,
	'RECURRENT',
	categoria.id as category_id,
	agofer.state,
	--agofer.contract_id,
	3,
	agofer.approve_date,
	agofer.date_from,
	agofer.date_to,
	agofer.valor,
	agofer.company_id,
	agofer.create_uid,
	agofer.create_date,
	agofer.write_uid,
	agofer.write_date
FROM dblink('dbname=agofer_08', 'SELECT
	conceptos.name AS name,
	categoria.code AS category_code,
	conceptos.category_id AS category_id,
	conceptos.state AS state,
	conceptos.contract_id AS contract_id,
	conceptos.approve_date AS approve_date,
	conceptos.date_from AS date_start,
	conceptos.date_to AS date_end,
	conceptos.valor AS amount,
	conceptos.company_id AS company_id,
	conceptos.create_uid AS create_uid,
	conceptos.create_date AS create_date,
	conceptos.write_uid AS write_uid,
	conceptos.write_date AS write_date
FROM
	hr_payroll_obligacion_tributaria AS conceptos
INNER JOIN
	hr_payroll_obligacion_tributaria_category AS categoria ON categoria.id = conceptos.category_id
WHERE
	categoria.concept_category IS NOT null'
) AS agofer(
	name character varying,
	category_code character varying,
	category_id integer,
	state character varying,
	contract_id integer,
	approve_date date,
	date_from date,
	date_to date,
	valor double precision,
	company_id integer,
	create_uid integer,
	create_date timestamp without time zone,
	write_uid integer,
	write_date timestamp without time zone
)
INNER JOIN hr_novelty_type as categoria on categoria.code = agofer.category_code;

select setval('hr_novelty_id_seq', (select max(id) from hr_novelty));
