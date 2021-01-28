insert into hr_period (name) values ('Indefinido')

INSERT INTO hr_payslip(
    id,
    name,
    state,
    contract_id,
    liquidation_date,
    accounting_date,
    company_id,
    period_id,
    payslip_type_id,
    payslip_processing_id,
    error_log,
    create_uid,
    create_date,
    write_uid,
    write_date,
	journal_id
) SELECT
    agofer.id,
    agofer.number,
    --agofer.state
    (case when agofer.state = 'done' then 'paid' else 'draft' end),
    agofer.contract_id,
    agofer.liquidacion_date,
    agofer.liquid_date,
    --agofer.company_id
    1,
    case when agofer.payslip_period_id is null then (select max(id) from hr_period) else agofer.payslip_period_id end,
    agofer.tipo_nomina,
    agofer.payslip_run_id,
    --agofer.payslip_processing_id
    null,
    agofer.create_uid,
    agofer.create_date,
    agofer.write_uid,
    agofer.write_date,
	agofer.journal_id
FROM dblink('dbname=agofer_08','select
        id,
        number,
        state,
        contract_id,
        liquidacion_date,
        liquid_date,
        payslip_period_id,
        tipo_nomina,
        payslip_run_id,
        create_uid,
        create_date,
        write_uid,
        write_date,
		journal_id
        from hr_payslip;'
) as agofer(
        id integer,
        number character varying,
        state character varying,
        contract_id integer,
        liquidacion_date date,
        liquid_date date,
        payslip_period_id integer,
        tipo_nomina integer,
        payslip_run_id integer,
		create_uid integer,
        create_date timestamp without time zone,
		write_uid integer,
        write_date timestamp without time zone,
		journal_id integer
)
WHERE agofer.id NOT IN (SELECT id FROM hr_payslip);

SELECT setval('hr_payslip_id_seq',(SELECT MAX(id)FROM hr_payslip));