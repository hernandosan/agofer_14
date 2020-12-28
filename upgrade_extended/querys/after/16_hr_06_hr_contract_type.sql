INSERT INTO hr_contract_type (
	id,
    create_uid,
    create_date,
    name,
    write_uid,
    write_date,
    term,
    section,
    type_class,
    company_id
) SELECT
	agofer.id,
    agofer.create_uid,
    agofer.create_date,
    agofer.name,
    agofer.write_uid,
    agofer.write_date,
    --agofer.term,
	(CASE WHEN agofer.term IS NULL THEN 'null' ELSE agofer.term END),
    --agofer.section,
	(CASE WHEN agofer.section IS NULL THEN 'null' ELSE agofer.section END),
    --agofer.type_class,
	(CASE WHEN agofer.type_class IS NULL THEN 'null' ELSE agofer.type_class END),
    --agofer.company_id
    1
FROM dblink('dbname=agofer_08','select
	id,
    create_uid,
    create_date,
    name,
    write_uid,
    write_date,
    (case when term = ''obralabor'' then ''obra-labor'' else term end),
    (case when section = ''administrativa'' then ''adm''
          when section = ''comercial'' then ''com''
          when section = ''operativa'' then ''ope''
          else section end),
    type_class
	from hr_contract_type;'
) AS agofer (
	id integer,
    create_uid integer,
    create_date timestamp without time zone,
    name character varying,
    write_uid integer,
    write_date timestamp without time zone,
    term character varying,
    section character varying,
    type_class character varying
);

select setval('hr_contract_type_id_seq', (select max(id) from hr_contract_type));