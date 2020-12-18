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
    write_date
) SELECT
    agofer.id,
    agofer.number,
    --agofer.state
    (case when v8.state = 'done' then 'paid' else 'draft' end),
    agofer.contract_id,
    agofer.liquidacion_date,
    agofer.liquid_date,
    --agofer.company_id
    1,
    agofer.payslip_period_id,
    agofer.tipo_nomina,
    agofer.payslip_run_id,
    --agofer.payslip_processing_id
    null,
    agofer.create_uid,
    agofer.create_date,
    agofer.write_uid,
    agofer.write_date
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
        write_date
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
        create_date timestamp without time zone,
        write_date timestamp without time zone
)
WHERE agofer.id NOT IN (SELECT id FROM hr_payslip);

SELECT setval('hr_payslip_id_seq',(SELECT MAX(id)FROM hr_payslip));

SELECT setval('hr_payslip_processing_id_seq',(SELECT MAX(id)FROM hr_payslip_processing));