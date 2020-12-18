INSERT INTO hr_period (
	id, 
    create_date,
    write_uid,
    write_date,
    create_uid,
    name,
    active,
    start,
    "end",
    type_period,
    type_biweekly,
    company_id
) SELECT
	agofer.id,
    agofer.create_date,
    agofer.write_uid,
    agofer.write_date,
    agofer.create_uid,
    agofer.name,
    NOT agofer.closed,
    agofer.start_period,
    agofer.end_period,
    --agofer.type_period,
    (case when agofer.schedule_pay = 'monthly' then 'MONTHLY' when agofer.schedule_pay = 'bi-monthly' then 'BIWEEKLY' else null end),
    --agofer.type_biweekly,
    (case when agofer.bm_type = 'first' then 'FIRST' when agofer.bm_type = 'second' then 'SECOND' else null end),
    --agofer.company_id,
    1
FROM dblink('dbname=agofer_08','select
	id,
    create_date,
    write_uid,
    write_date,
    create_uid,
    name,
    closed,
    start_period,
    end_period,
    schedule_pay,
    bm_type
	from payslip_period;'
) AS agofer(
	id integer,
    create_date timestamp without time zone,
    write_uid integer,
    write_date timestamp without time zone,
    create_uid integer,
    name character varying,
    closed boolean,
    start_period date,
    end_period date,
    schedule_pay character varying,
    bm_type character varying
);

select setval('hr_period_id_seq', (select max(id) from hr_period));