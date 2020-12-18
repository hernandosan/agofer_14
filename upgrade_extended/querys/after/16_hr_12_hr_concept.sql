INSERT INTO hr_concept (
	id,
	name,
	code,
	partner_type,
	partner_id,
	category,
	company_id,
	create_uid,
	create_date,
	write_uid,
	write_date
) SELECT
	agofer.id,
	agofer.name,
	agofer.code,
	agofer.partner_type,
	agofer.partner_other,
	agofer.category,
	--agofer.company_id
	1,
	agofer.create_uid,
	agofer.create_date,
	agofer.write_uid,
	agofer.write_date
FROM dblink('dbname=agofer_08', 'SELECT
	concepto.id AS id,
	concepto.name AS name,
	concepto.code AS code,
	concepto.partner_type AS partner_type,
	concepto.partner_other AS partner_id,
	concepto.category AS category,
	concepto.create_uid AS create_uid,
	concepto.create_date AS create_date,
	concepto.write_uid AS write_uid,
	concepto.write_date AS write_date
FROM
	hr_concept AS concepto'
) AS agofer(
	id integer,
	name character varying,
	code character varying,
	partner_type character varying,
	partner_other integer,
	category character varying,
	create_uid integer,
	create_date timestamp without time zone,
	write_uid integer,
	write_date timestamp without time zone
)
WHERE agofer.id NOT IN (SELECT id FROM hr_concept);

select setval('hr_concept_id_seq', (select max(id) from hr_concept));