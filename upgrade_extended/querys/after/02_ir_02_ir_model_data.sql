insert into ir_model_data (
	create_uid, 
	create_date, 
	write_date, 
	write_uid, 
	noupdate, 
	name, 
	module, 
	model, 
	res_id
)
select 
	agofer.create_uid, 
	agofer.create_date, 
	agofer.write_date, 
	agofer.write_uid, 
	agofer.noupdate, 
	agofer.name, 
	agofer.module, 
	agofer.model, 
	agofer.res_id 
from dblink('dbname=agofer_08', 'select 
			create_uid, 
			create_date, 
			write_date, 
			write_uid, 
			noupdate, 
			name, 
			module, 
			model, 
			res_id 
			from ir_model_data;') as agofer(
	create_uid integer, 
	create_date timestamp without time zone, 
	write_date timestamp without time zone, 
	write_uid integer, 
	noupdate boolean, 
	name character varying, 
	module character varying, 
	model character varying, 
	res_id integer) 
left join ir_module_module imm on imm.name = agofer.module 
where imm.name is null 
and agofer.module like '%agofer%';