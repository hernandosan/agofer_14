insert into helpdesk_ticket_team (
	id, 
	create_uid, 
	create_date, 
	name, 
	write_uid, 
	write_date,
	alias_id
	)
select 
	agofer.id, 
	agofer.create_uid, 
	agofer.create_date, 
	agofer.name, 
	agofer.write_uid, 
	agofer.write_date,
	3
from dblink('dbname=agofer_08','SELECT 
	id, 
	create_uid, 
	create_date, 
	name, 
	write_uid, 
	write_date
	FROM website_support_ticket_categories;'
) as agofer(
	id integer, 
	create_uid integer, 
	create_date timestamp without time zone, 
	name character varying, 
	write_uid integer, 
	write_date timestamp without time zone
);

