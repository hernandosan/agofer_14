INSERT INTO hr_overtime_type (
	id,
	rate,
	name,
	code,
	category,
	partner_type,
	partner_id,
	company_id,
	create_uid,
	create_date,
	write_uid,
	write_date
) SELECT
	agofer.id,
	agofer.multiplicador,
	agofer.name,
	agofer.code,
	agofer.concept_category,
	agofer.partner_type,
	agofer.partner_id,
	--agofer.company_id
	1,
	agofer.create_uid,
	agofer.create_date,
	agofer.write_uid,
	agofer.write_date
FROM dblink('dbname=agofer_08', 'SELECT
	categoria.id as id,
	categoria.multiplicador AS multiplicador,
	categoria.name AS name,
	categoria.code AS code,
	categoria.concept_category AS concept_category,
	categoria.partner_type AS partner_type,
	categoria.partner_id AS partner_id,
	categoria.create_uid AS create_uid,
	categoria.create_date AS create_date,
	categoria.write_uid AS write_uid,
	categoria.write_date AS write_date
FROM hr_payroll_extrahours_type AS categoria'
) AS agofer(
	id integer,
	multiplicador double precision,
	name character varying,
	code character varying,
	concept_category character varying,
	partner_type character varying,
	partner_id integer,
	create_uid integer,
	create_date timestamp without time zone,
	write_uid integer,
	write_date timestamp without time zone
)
WHERE agofer.id NOT IN (SELECT id FROM hr_overtime_type);

select setval('hr_overtime_type_id_seq', (select max(id) from hr_overtime_type));