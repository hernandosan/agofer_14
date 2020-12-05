insert into account_move (
	id, 
	create_uid, 
	create_date, 
	name, 
	state, 
	write_uid, 
	ref, 
	company_id, 
	journal_id, 
	write_date, 
	narration, 
	date, 
	partner_id, 
	to_check,
	move_type,
	currency_id,
	reference_type
	)
select 
	agofer.id, 
	agofer.create_uid, 
	agofer.create_date, 
	agofer.name, 
	agofer.state, 
	agofer.write_uid, 
	agofer.ref, 
	agofer.company_id, 
	agofer.journal_id,
	agofer.write_date, 
	agofer.narration, 
	agofer.date, 
	agofer.partner_id, 
	agofer.to_check,
	--agofer.move_type
	'entry',
	--agofer.currency_id
	8,
	--agofer.reference_type
	'none'
from dblink('dbname=agofer_08','SELECT 
	am.id, 
	am.create_uid, 
	am.create_date, 
	am.name, 
	am.state, 
	am.write_uid, 
	am.ref, 
	am.company_id, 
	am.journal_id, 
	am.write_date, 
	am.narration, 
	am.date, 
	am.partner_id, 
	am.to_check
	FROM account_move am
	INNER JOIN account_journal aj ON aj.id = am.journal_id
	WHERE aj.niif = False;'
) as agofer(
	id integer, 
	create_uid integer, 
	create_date timestamp without time zone, 
	name character varying, 
	state character varying, 
	write_uid integer, 
	ref character varying, 
	company_id integer, 
	journal_id integer, 
	write_date timestamp without time zone, 
	narration text, 
	date date, 
	partner_id integer, 
	to_check boolean
) WHERE cast(agofer.date as date) >= '2019-01-01';

select setval('account_move_id_seq', (select max(id) from account_move));