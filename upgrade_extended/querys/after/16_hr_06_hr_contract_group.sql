INSERT INTO hr_contract_group (
	id, 
    create_uid,
    create_date,
    name,
    write_uid,
    write_date,
    company_id
) SELECT
	agofer.id, 
    agofer.create_uid,
    agofer.create_date,
    agofer.name,
    agofer.write_uid,
    agofer.write_date,
    --agofer.company_id
    1
FROM dblink('dbname=agofer_08','select
	id, 
    create_uid,
    create_date,
    name,
    write_uid,
    write_date
	from hr_contract_group;'
) AS agofer(
	id integer, 
    create_uid integer,
    create_date timestamp without time zone,
    name character varying,
    write_uid integer,
    write_date timestamp without time zone
);

select setval('hr_contract_group_id_seq', (select max(id) from hr_contract_group));