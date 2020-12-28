ALTER TABLE hr_contract_risk DISABLE TRIGGER ALL;
DELETE FROM hr_contract_risk;
ALTER TABLE hr_contract_risk ENABLE TRIGGER ALL;

INSERT INTO hr_contract_risk (
	id, 
    create_uid,
    create_date,
    name,
    write_uid,
    risk_percentage,
    write_date
) SELECT
	agofer.id, 
    agofer.create_uid,
    agofer.create_date,
    agofer.name,
    agofer.write_uid,
    agofer.pct_risk,
    agofer.write_date
FROM dblink('dbname=agofer_08','select
	id, 
    create_uid,
    create_date,
    name,
    write_uid,
    pct_risk,
    write_date
	from hr_contract_risk;'
) AS agofer(
	id integer, 
    create_uid integer,
    create_date timestamp without time zone,
    name character varying,
    write_uid integer,
    pct_risk numeric,
    write_date timestamp without time zone
);

select setval('hr_contract_risk_id_seq', (select max(id) from hr_contract_risk));