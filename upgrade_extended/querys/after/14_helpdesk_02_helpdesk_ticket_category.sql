insert into helpdesk_ticket_category (
	id, 
	active, 
	name, 
	create_uid, 
	create_date, 
	write_uid, 
	write_date, 
	team_id
	)
select 
	agofer.id, 
	agofer.active, 
	agofer.name, 
	agofer.create_uid, 
	agofer.create_date, 
	agofer.write_uid, 
	agofer.write_date, 
	agofer.category_id
from dblink('dbname=agofer_08','SELECT 
	id,
	active, 
	name,
	create_uid, 
	create_date, 
	write_uid, 
	write_date, 
	category_id
	FROM website_support_ticket_platforms;'
) as agofer(
	id integer,
	active boolean, 
	name character varying, 
	create_uid integer, 
	create_date timestamp without time zone, 
	write_uid integer, 
	write_date timestamp without time zone, 
	category_id integer
);

