insert into mail_alias (
	id, 
	create_uid, 
	alias_parent_thread_id, 
	write_uid, 
	alias_defaults, 
	alias_contact, 
	alias_parent_model_id, 
	alias_user_id, 
	alias_force_thread_id, 
	alias_model_id, 
	write_date, 
	create_date, 
	alias_name
) select 
	agofer.id, 
	agofer.create_uid, 
	agofer.alias_parent_thread_id, 
	agofer.write_uid, 
	agofer.alias_defaults, 
	agofer.alias_contact, 
	agofer.alias_parent_model_id, 
	agofer.alias_user_id, 
	agofer.alias_force_thread_id, 
	agofer.alias_model_id, 
	agofer.write_date, 
	agofer.create_date, 
	--agofer.alias_name,
	cast(agofer.id as character varying)
from dblink('dbname=agofer_08','SELECT 
	id, 
	create_uid, 
	alias_parent_thread_id, 
	write_uid, 
	alias_defaults, 
	alias_contact, 
	alias_parent_model_id, 
	alias_user_id, 
	alias_force_thread_id, 
	alias_model_id, 
	write_date, 
	create_date, 
	alias_name
	FROM mail_alias;'
) as agofer(
	id integer, 
	create_uid integer, 
	alias_parent_thread_id integer, 
	write_uid integer, 
	alias_defaults text, 
	alias_contact character varying, 
	alias_parent_model_id integer, 
	alias_user_id integer, 
	alias_force_thread_id integer, 
	alias_model_id integer, 
	write_date timestamp without time zone, 
	create_date timestamp without time zone, 
	alias_name character varying
)inner join ir_model im1 on im1.id = agofer.alias_model_id 
inner join ir_model im2 on im2.id = agofer.alias_parent_model_id
where agofer.id not in (select id from mail_alias);

select setval('mail_alias_id_seq', (select max(id) from mail_alias));