INSERT INTO hr_payslip_line(
    category,
    concept_id,
    create_date,
    create_uid,
    id,
    name,
    origin,
    payslip_id,
    qty,
    rate,
    total,
    value,
    write_date,
    write_uid
) SELECT *
FROM dblink('dbname=agofer_08', 'select
    category,
    concept_id,
    create_date,
    create_uid,
    id,
    name,
    ''import'',
    payslip_id,
    qty,
    rate,
    total,
    amount,
    write_date,
    write_uid
    from hr_payslip_concept;'
) AS agofer(
    category character varying,
    concept_id integer,
    create_date timestamp without time zone,
    create_uid integer,
    id integer,
    name character varying,
    origin character varying,
    payslip_id integer,
    qty double precision,
    rate double precision,
    total double precision,
    value double precision,
    write_date timestamp without time zone,
    write_uid integer
);

SELECT setval('hr_payslip_line_id_seq',(SELECT MAX(id) FROM hr_payslip_line);