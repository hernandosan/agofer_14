INSERT INTO ir_sequence (
	id, 
	create_uid, 
	code, 
	create_date, 
	suffix, 
	number_next, 
	number_increment, 
	implementation, 
	company_id, 
	write_uid, 
	padding, 
	active, 
	prefix, 
	write_date, 
	name
) SELECT
	agofer.id, 
	agofer.create_uid, 
	agofer.code, 
	agofer.create_date, 
	agofer.suffix, 
	agofer.number_next, 
	agofer.number_increment, 
	agofer.implementation, 
	agofer.company_id, 
	agofer.write_uid, 
	agofer.padding, 
	agofer.active, 
	agofer.prefix, 
	agofer.write_date, 
	agofer.name 
FROM dblink('dbname=agofer_08', 'select
	id, 
	create_uid, 
	code, 
	create_date, 
	suffix, 
	number_next, 
	number_increment, 
	implementation, 
	company_id, 
	write_uid, 
	padding, 
	active, 
	prefix, 
	write_date, 
	name
	from ir_sequence;'
) AS agofer(
	id integer, 
	create_uid integer, 
	code character varying, 
	create_date timestamp without time zone, 
	suffix character varying, 
	number_next integer, 
	number_increment integer, 
	implementation character varying, 
	company_id integer, 
	write_uid integer, 
	padding integer, 
	active boolean, 
	prefix character varying, 
	write_date timestamp without time zone, 
	name character varying
)
WHERE agofer.id NOT IN (SELECT id FROM ir_sequence);

select setval('ir_sequence_id_seq', (select max(id) from ir_sequence));