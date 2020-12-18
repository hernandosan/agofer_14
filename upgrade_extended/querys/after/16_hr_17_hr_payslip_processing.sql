INSERT INTO hr_payslip_processing(
    id,
    name,
    state,
    company_id,
    period_id,
    liquidation_date,
    accounting_date,
    payslip_type_id,
    contract_group_id,
    error_log,
    create_uid,
    create_date,
    write_uid,
    write_date
) SELECT
    agofer.id,
    agofer.name,
    --agofer.state
    (case when v8.state = 'draft' then 'draft' when v8.state = 'close' then 'paid' else 'draft' end),
    --agofer.company
    1,
    agofer.payslip_period,
    --agofer.liquidation_date
    COALESCE(v8.date_liquidacion,v8.date_acc),
    agofer.date_acc,
    agofer.tipo_nomina,
    --agofer.contract_group_id
    null,
    --agofer.error_log
    null,
    agofer.create_uid,
    agofer.create_date
    agofer.write_uid,
    agofer.write_date
FROM dblink('dbname=agofer_08',' select
        id,
        name,
        state,
        payslip_period,
        date_liquidacion,
        date as date_acc,
        tipo_nomina,
        write_date
        from hr_payslip_run;'
) AS agofer (
        id integer,
        name character varying,
        state character varying,
        payslip_period integer,
        date_liquidacion date,
        date_acc date,
        tipo_nomina integer,
        write_date timestamp without time zone
)
WHERE agofer.id NOT IN (SELECT id FROM hr_payslip_processing);

SELECT setval('hr_payslip_processing_id_seq',(SELECT MAX(id)FROM hr_payslip_processing));