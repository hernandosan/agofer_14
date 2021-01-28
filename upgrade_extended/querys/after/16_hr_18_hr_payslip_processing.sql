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
    write_date,
	journal_id
) SELECT
    agofer.id,
    agofer.name,
    --agofer.state
    (case when agofer.state = 'draft' then 'draft' when agofer.state = 'close' then 'paid' else 'draft' end),
    --agofer.company
    1,
    agofer.payslip_period,
    --agofer.liquidation_date
    COALESCE(agofer.date_liquidacion,agofer.date_acc),
    agofer.date_acc,
    agofer.tipo_nomina,
    --agofer.contract_group_id
    null,
    --agofer.error_log
    null,
    agofer.create_uid,
    agofer.create_date,
    agofer.write_uid,
    agofer.write_date,
	agofer.journal_id
FROM dblink('dbname=agofer_08',' select
        id,
        name,
        state,
        payslip_period,
        date_liquidacion,
        date as date_acc,
        tipo_nomina,
		create_uid,
		create_date,
		write_uid,
        write_date,
		journal_id
        from hr_payslip_run;'
) AS agofer (
        id integer,
        name character varying,
        state character varying,
        payslip_period integer,
        date_liquidacion date,
        date_acc date,
        tipo_nomina integer,
		create_uid integer,
		create_date timestamp without time zone,
		write_uid integer,
        write_date timestamp without time zone,
	    journal_id integer
)
WHERE agofer.id NOT IN (SELECT id FROM hr_payslip_processing);

SELECT setval('hr_payslip_processing_id_seq',(SELECT MAX(id)FROM hr_payslip_processing));