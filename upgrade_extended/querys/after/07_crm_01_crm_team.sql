ALTER TABLE crm_team DISABLE TRIGGER ALL;
DELETE FROM crm_team;
ALTER TABLE crm_team ENABLE TRIGGER ALL;

INSERT INTO crm_team (
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
	invoiced_target,
	alias_id,
    use_leads,
    use_opportunities,
	company_id
) SELECT
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
	--agofer.alias_id,
	1,
    agofer.use_leads,
    agofer.use_opportunities,
	--agofer.company_id
	1
FROM dblink('dbname=agofer_08','select
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
	invoiced_target,
	alias_id,
    use_leads,
    use_opportunities
	from crm_case_section;'
) AS agofer(
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
	invoiced_target integer,
	alias_id integer,
    use_leads boolean,
    use_opportunities boolean
);

select setval('crm_team_id_seq', (select max(id) from crm_team));

update account_move as am 
set team_id = agofer.section_id 
from dblink('dbname=agofer_08','select move_id, section_id from account_invoice where section_id is not null') as agofer 
(move_id integer, section_id integer) 
where am.id = agofer.move_id;