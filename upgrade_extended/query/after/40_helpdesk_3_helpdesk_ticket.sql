insert into helpdesk_ticket (
	id, 
	number, 
	name,
	description, 
	user_id, 
	stage_id, 
	partner_id, 
	closed_date, 
	company_id, 
	category_id, 
	team_id, 
	priority, 
	create_uid, 
	create_date, 
	write_uid, 
	write_date, 
	type_id,
	active
	)
select 
	agofer.id, 
	agofer.number, 
	agofer.name,
	agofer.description, 
	agofer.user_id, 
	agofer.state, 
	agofer.partner_id, 
	agofer.close_date, 
	agofer.company_id, 
	agofer.platform, 
	agofer.category, 
	agofer.priority, 
	agofer.create_uid, 
	agofer.create_date,
	agofer.write_uid, 
	agofer.write_date, 
	agofer.subcategory,
	--agofer.active
	'True'
from dblink('dbname=agofer_08','SELECT 
	id,
	name as number,
	name,
	description,
	user_id,
	state,
	partner_id,
	close_date,
	company_id,
	platform,
	category,
	priority,
	create_uid,
	create_date,
	write_uid,
	write_date,
	subcategory
	FROM website_support_ticket
	WHERE description IS NOT NULL;'
) as agofer(
	id integer,
	number character varying,
	name character varying, 
	description text, 
	user_id integer, 
	state integer, 
	partner_id integer, 
	close_date timestamp without time zone, 
	company_id integer, 
	platform integer, 
	category integer, 
	priority character varying, 
	create_uid integer, 
	create_date timestamp without time zone, 
	write_uid integer, 
	write_date timestamp without time zone, 
	subcategory integer
);
