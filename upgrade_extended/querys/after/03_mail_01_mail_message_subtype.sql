INSERT INTO mail_message_subtype (
	id,
	create_uid,
	create_date,
	name,
	res_model,
	write_uid,
	parent_id,
	write_date,
	relation_field,
	hidden,
	description,
	sequence
)SELECT
	agofer.id,
	agofer.create_uid,
	agofer.create_date,
	agofer.name,
	agofer.res_model,
	agofer.write_uid,
	agofer.parent_id,
	agofer.write_date,
	agofer.relation_field,
	agofer.hidden,
	agofer.description,
	agofer.sequence
FROM dblink('dbname=agofer_08','SELECT
	id,
	create_uid,
	create_date,
	name,
	res_model,
	write_uid,
	parent_id,
	write_date,
	relation_field,
	hidden,
	description,
	sequence
	FROM mail_message_subtype;'
) AS agofer(
	id integer,
	create_uid integer,
	create_date timestamp without time zone,
	name character varying,
	res_model character varying,
	write_uid integer,
	parent_id integer,
	write_date timestamp without time zone,
	relation_field character varying,
	hidden boolean,
	description text,
	sequence double precision
) 
WHERE agofer.id NOT IN (SELECT id FROM mail_message_subtype);

select setval('mail_message_subtype_id_seq', (select max(id) from mail_message_subtype));