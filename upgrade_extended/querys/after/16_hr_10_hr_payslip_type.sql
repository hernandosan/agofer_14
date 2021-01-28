INSERT INTO hr_payslip_type (
	id,
	name,
	company_id,
	create_uid,
	create_date,
	write_uid,
	write_date,
	category
) SELECT
    agofer.id,
	agofer.name,
	--agofer.company_id
	1,
	agofer.create_uid,
	agofer.create_date,
	agofer.write_uid,
	agofer.write_date,
	--agofer.category
	(case when agofer.code = 'Nomina' then 'NOM'
         when agofer.code = 'Vacaciones' then 'VAC'
         when agofer.code = 'Liquidacion' then 'LIQ'
         when agofer.code = 'Cesantias' then 'CES'
         when agofer.code = 'Int. Cesantias' then 'INTE_CES'
         when agofer.code = 'Otros' then 'OTH'
         when agofer.code = 'Prima' then 'PRI'
         when agofer.code = 'CesantiasAnuales' then 'CES'
         when agofer.code = 'Provisiones' then 'CON'
         else 'OTH'
    end)
FROM dblink('dbname=agofer_08', 'select
	id,
	name,
	create_uid,
	create_date,
	write_uid,
	write_date,
	code
    from hr_payslip_type;'
) AS agofer(
	id integer,
	name character varying,
	create_uid integer,
	create_date timestamp without time zone,
	write_uid integer,
	write_date timestamp without time zone,
	code character varying
)
WHERE agofer.id NOT IN (SELECT id FROM hr_payslip_type);

select setval('hr_payslip_type_id_seq', (select max(id) from hr_payslip_type));

insert into hr_payslip_type_hr_concept_rel (hr_payslip_type_id, hr_concept_id) 
select agofer.type_id, agofer.concept_id 
from dblink('dbname=agofer_08',
            'select type_id, concept_id from paysliptype_concept_rel') as agofer(type_id integer, concept_id integer);