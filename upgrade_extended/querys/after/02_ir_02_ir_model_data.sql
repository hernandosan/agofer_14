-- INSERT INTO ir_model_data (
-- 	-- id,
-- 	create_uid,
-- 	create_date,
-- 	write_date,
-- 	write_uid,
-- 	noupdate,
-- 	name,
-- 	module,
-- 	model,
-- 	res_id
-- ) SELECT
-- 	-- agofer.id,
-- 	agofer.create_uid,
-- 	agofer.create_date,
-- 	agofer.write_date,
-- 	agofer.write_uid,
-- 	agofer.noupdate,
-- 	REPLACE(agofer.name, ' ', '_'),
-- 	agofer.module,
-- 	agofer.model,
-- 	agofer.res_id
-- FROM dblink('dbname=agofer_08', 'select
-- 	-- id,
--     create_uid,
--     create_date,
--     write_date,
--     write_uid,
--     noupdate,
--     name,
--     module,
--     model,
--     res_id
--     from ir_model_data;'
-- ) AS agofer(
-- 	-- id integer,
-- 	create_uid integer,
-- 	create_date timestamp without time zone,
-- 	write_date timestamp without time zone,
-- 	write_uid integer,
-- 	noupdate boolean,
-- 	name character varying,
-- 	module character varying,
-- 	model character varying,
-- 	res_id integer
-- ) inner join ir_model im on im.model = agofer.model 
-- inner join ir_module_module imm on imm.name = agofer.module 
-- left join ir_model_data imd on agofer.name = imd.name 
-- where agofer.name is null;

select id from ir_model_data;