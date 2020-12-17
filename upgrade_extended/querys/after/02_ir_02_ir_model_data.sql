INSERT INTO ir_model_data (
	create_uid,
	create_date,
	write_date,
	write_uid,
	noupdate,
	name,
	module,
	model,
	res_id
) SELECT
	agofer.create_uid,
	agofer.create_date,
	agofer.write_date,
	agofer.write_uid,
	agofer.noupdate,
	agofer.name,
	agofer.module,
	agofer.model,
	agofer.res_id
FROM dblink('dbname=agofer_08', 'select
    create_uid,
    create_date,
    write_date,
    write_uid,
    noupdate,
    name,
    module,
    model,
    res_id
    from ir_model_data;'
) AS agofer(
	create_uid integer,
	create_date timestamp without time zone,
	write_date timestamp without time zone,
	write_uid integer,
	noupdate boolean,
	name character varying,
	module character varying,
	model character varying,
	res_id integer
)
LEFT JOIN ir_module_module imm ON imm.name = agofer.module
WHERE imm.name IS NULL
AND agofer.module LIKE '%agofer%';

select setval('ir_model_data_id_seq', (select max(id) from ir_model_data));