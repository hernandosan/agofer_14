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
FROM dblink('dbname=agofer_08', 'select
	id,
	multiplicador,
	name,
	code,
	concept_category,
	partner_type,
	partner_id,
	create_uid,
	create_date,
	write_uid,
	write_date
    from hr_payroll_extrahours_type'
) AS agofer (
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