INSERT INTO hr_leave_type (
	id,
	name,
	code,
	category_type,
	category,
	b2,
	b90,
	b180,
	a180,
	company_id,
	create_uid,
	create_date,
	write_uid,
	write_date
) SELECT
	agofer.id,
	agofer.name,
	agofer.code,
	--agofer.category_type
	'VAC',
	agofer.concept_category,
	agofer.gi_b2,
	agofer.gi_b90,
	agofer.gi_b180,
	agofer.gi_a180,
	--agofer.company_id
	1,
	agofer.create_uid,
	agofer.create_date,
	agofer.write_uid,
	agofer.write_date
FROM dblink('dbname=agofer_08', 'SELECT
	ausencia.id AS id,
	ausencia.name AS name,
	ausencia.code AS code,
	ausencia.concept_category AS concept_category,
	ausencia.gi_b2 as gi_b2,
	ausencia.gi_b90 as gi_b90,
	ausencia.gi_b180 as gi_b180,
	ausencia.gi_a180 as gi_a180,
	ausencia.create_uid AS create_uid,
	ausencia.create_date AS create_date,
	ausencia.write_uid AS write_uid,
	ausencia.write_date AS write_date
    from hr_holidays_status AS ausencia
    where concept_category IS NOT NULL'
) AS agofer(
	id integer,
	name character varying,
	code character varying,
	concept_category character varying,
	gi_b2 double precision,
	gi_b90 double precision,
	gi_b180 double precision,
	gi_a180 double precision,
	create_uid integer,
	create_date timestamp without time zone,
	write_uid integer,
	write_date timestamp without time zone
)
WHERE agofer.id NOT IN (SELECT id FROM hr_leave_type);

select setval('hr_leave_type_id_seq', (select max(id) from hr_leave_type));

select setval('hr_novelty_id_seq', (select max(id) from hr_novelty));
