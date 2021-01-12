ALTER TABLE mail_message DISABLE TRIGGER ALL;
DELETE FROM mail_message;
ALTER TABLE mail_message ENABLE TRIGGER ALL;

INSERT INTO mail_message (
	id, 
	body, 
	record_name, 
	write_date, 
	mail_server_id, 
	write_uid, 
	no_auto_thread, 
	date, 
	create_date, 
	subject, 
	create_uid, 
	message_id, 
	parent_id, 
	res_id, 
	subtype_id, 
	reply_to, 
	author_id, 
	model, 
	email_from,
	message_type
) SELECT
	agofer.id, 
	agofer.body, 
	agofer.record_name, 
	agofer.write_date, 
	agofer.mail_server_id, 
	agofer.write_uid, 
	agofer.no_auto_thread, 
	agofer.date, 
	agofer.create_date, 
	agofer.subject, 
	agofer.create_uid, 
	agofer.message_id, 
	agofer.parent_id,
	agofer.res_id, 
	agofer.subtype_id, 
	agofer.reply_to, 
	agofer.author_id, 
	agofer.model, 
	agofer.email_from,
    (case when agofer.type IS null then 'null' when agofer.type IS NOT null THEN agofer.type end)
FROM dblink('dbname=agofer_08', 'select
	id,
	body,
	record_name,
	write_date,
	mail_server_id,
	write_uid,
	no_auto_thread,
	date,
	create_date,
	subject,
	create_uid,
	message_id,
	parent_id,
	res_id,
	subtype_id,
	reply_to,
	author_id,
	model,
	email_from,
	type
	from mail_message;'
) AS agofer(
	id integer,
	body text,
	record_name character varying,
	write_date timestamp without time zone,
	mail_server_id integer,
	write_uid integer,
	no_auto_thread boolean,
	date timestamp without time zone,
	create_date timestamp without time zone,
	subject character varying,
	create_uid integer,
	message_id character varying,
	parent_id integer,
	res_id integer,
	subtype_id integer,
	reply_to character varying,
	author_id integer,
	model character varying,
	email_from character varying,
	type character varying
)inner join ir_model im on im.model = agofer.model;

select setval('mail_message_id_seq', (select max(id) from mail_message));