INSERT INTO hr_novelty (
	name,
	type_novelty,
	novelty_type_id,
	state,
	contract_id,
	approve_date,
	amount,
	date_start,
	company_id,
	create_uid,
	create_date,
	write_uid,
	write_date
) SELECT
	agofer.name,
	--agofer.type_novelty,
	'STATIC',
	--agofer.novelty_type_id
	categoria.id as category_id,
	agofer.state,
	--agofer.contract_id,
	3,
	agofer.approve_date,
	agofer.amount,
	agofer.date,
	agofer.company_id,
	--agofer.create_uid,
	2,
	agofer.create_date,
	--agofer.write_uid,
	2,
	agofer.write_date
FROM dblink('dbname=agofer_08', 'SELECT
	novedades.name AS name,
	categoria.code AS category_code,
	novedades.category_id AS category_id,
	novedades.state AS state,
	novedades.contract_id AS contract_id,
	novedades.approve_date AS approve_date,
	novedades.total AS amount,
	novedades.date AS date_start,
	novedades.company_id AS company_id,
	novedades.create_uid AS create_uid,
	novedades.create_date AS create_date,
	novedades.write_uid AS write_uid,
	novedades.write_date AS write_date
    from hr_payroll_novedades AS novedades
    inner join hr_payroll_novedades_category AS categoria ON categoria.id = novedades.category_id
    where categoria.concept_category IS NOT null'
) AS agofer(
	name character varying,
	category_code character varying,
	category_id integer,
	state character varying,
	contract_id integer,
	approve_date date,
	amount double precision,
	date date,
	company_id integer,
	create_uid integer,
	create_date timestamp without time zone,
	write_uid integer,
	write_date timestamp without time zone
)
INNER JOIN hr_novelty_type as categoria on categoria.code = agofer.category_code;

select setval('hr_novelty_id_seq', (select max(id) from hr_novelty));