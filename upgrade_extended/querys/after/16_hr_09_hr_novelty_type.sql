INSERT INTO hr_novelty_type (
	name,
	code,
	partner_type,
	partner_id,
	category,
	-- reg_adm_debit,
	-- reg_adm_credit,
	-- reg_com_debit,
	-- reg_com_credit,
    	-- reg_ope_debit,
    	-- reg_ope_credit,
    	-- int_adm_debit,
    	-- int_adm_credit,
    	-- int_com_debit,
    	-- int_com_credit,
    	-- int_ope_debit,
    	-- int_ope_credit,
    	-- apr_adm_debit,
    	-- apr_adm_credit,
    	-- apr_com_debit,
    	-- apr_com_credit,
    	-- apr_ope_debit,
    	-- apr_ope_credit,
	company_id,
	create_uid,
	create_date,
	write_uid,
	write_date
) SELECT
	agofer.name,
	agofer.code,
	agofer.partner_type,
	agofer.partner_id,
	agofer.category,
	--agofer.reg_adm_debit,
	--agofer.reg_adm_credit,
	--agofer.reg_com_debit,
	--agofer.reg_com_credit,
       	--agofer.reg_ope_debit,
    	--agofer.reg_ope_credit,
    	--agofer.int_adm_debit,
    	--agofer.int_adm_credit,
    	--agofer.int_com_debit,
    	--agofer.int_com_credit,
    	--agofer.int_ope_debit,
    	--agofer.int_ope_credit,
    	--agofer.apr_adm_debit,
    	--agofer.apr_adm_credit,
    	--agofer.apr_com_debit,
    	--agofer.apr_com_credit,
    	--agofer.apr_ope_debit,
    	--agofer.apr_ope_credit,
	1, -- company_id
	agofer.create_uid,
	agofer.create_date,
	agofer.write_uid,
	agofer.write_date
FROM dblink('dbname=agofer_08', 'SELECT
	novedad.name as name,
	novedad.code as code,
	novedad.partner_type as partner_type,
	novedad.partner_id as partner_id,
	novedad.concept_category as category,
	novedad.reg_adm_debit AS reg_adm_debit,
	novedad.reg_adm_credit AS reg_adm_credit,
	novedad.reg_com_debit AS reg_com_debit,
	novedad.reg_com_credit AS reg_com_credit,
    	novedad.reg_ope_debit AS reg_ope_debit,
    	novedad.reg_ope_credit AS reg_ope_credit,
    	novedad.int_adm_debit AS int_adm_debit,
    	novedad.int_adm_credit AS int_adm_credit,
    	novedad.int_com_debit AS int_com_debit,
    	novedad.int_com_credit AS int_com_credit,
    	novedad.int_ope_debit AS int_ope_debit,
    	novedad.int_ope_credit AS int_ope_credit,
    	novedad.apr_adm_debit AS apr_adm_debit,
    	novedad.apr_adm_credit AS apr_adm_credit,
    	novedad.apr_com_debit AS apr_com_debit,
    	novedad.apr_com_credit AS apr_com_credit,
    	novedad.apr_ope_debit AS apr_ope_debit,
    	novedad.apr_ope_credit AS apr_ope_credit,
	novedad.create_uid AS create_uid,
	novedad.create_date AS create_date,
	novedad.write_uid AS write_uid,
	novedad.write_date AS write_date
FROM
	hr_payroll_novedades_category AS novedad
WHERE
	novedad.concept_category IS NOT NULL'
) AS agofer(
	name character varying,
	code character varying,
	partner_type character varying,
	partner_id integer,
	category character varying,
	reg_adm_debit integer,
	reg_adm_credit integer,
	reg_com_debit integer,
	reg_com_credit integer,
    	reg_ope_debit integer,
    	reg_ope_credit integer,
    	int_adm_debit integer,
    	int_adm_credit integer,
    	int_com_debit integer,
    	int_com_credit integer,
    	int_ope_debit integer,
    	int_ope_credit integer,
    	apr_adm_debit integer,
    	apr_adm_credit integer,
    	apr_com_debit integer,
    	apr_com_credit integer,
    	apr_ope_debit integer,
    	apr_ope_credit integer,
	create_uid integer,
	create_date timestamp without time zone,
	write_uid integer,
	write_date timestamp without time zone
)
WHERE agofer.code NOT IN (SELECT code FROM hr_novelty_type);

select setval('hr_novelty_type_id_seq', (select max(id) from hr_novelty_type));