insert into crm_team (
	id, 
	color, 
	write_uid, 
	write_date, 
	active, 
	create_date, 
	create_uid, 
	user_id, 
	name, 
	use_quotations, 
	invoiced_target
	alias_id
) select 
	agofer.id, 
	agofer.color, 
	agofer.write_uid, 
	agofer.write_date, 
	agofer.active, 
	agofer.create_date, 
	agofer.create_uid, 
	agofer.user_id, 
	agofer.name, 
	agofer.use_quotations, 
	agofer.invoiced_target,
	1
from dblink('dbname=agofer_08','SELECT 
	id, 
	color, 
	write_uid, 
	write_date, 
	active, 
	create_date, 
	create_uid, 
	user_id, 
	name, 
	use_quotations, 
	invoiced_target
	FROM crm_case_section;'
) as agofer(
	id integer, 
	color integer, 
	write_uid integer, 
	write_date timestamp without time zone, 
	active boolean, 
	create_date timestamp without time zone, 
	create_uid integer, 
	user_id integer, 
	name character varying, 
	use_quotations boolean, 
	invoiced_target integer
) where agofer.id not in (select id from crm_team);

select setval('crm_team_id_seq', (select max(id) from crm_team));