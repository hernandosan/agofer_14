INSERT INTO account_move (
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
	currency_id,
	move_type
	)
SELECT
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
	--agofer.currency_id
	9,
	--agofer.move_type
	'entry'
FROM dblink('dbname=agofer_08','select
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
	to_check
	from account_move;'
) AS agofer(
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
);

select setval('account_move_id_seq', (select max(id) from account_move));