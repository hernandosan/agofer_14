ALTER TABLE res_bank DISABLE TRIGGER ALL;
DELETE FROM res_bank;
ALTER TABLE res_bank ENABLE TRIGGER ALL;

INSERT INTO res_bank (
	id, 
	city, 
	create_date, 
	name, 
	zip, 
	create_uid, 
	country, 
	street2, 
	bic, 
	phone, 
	state, 
	street, 
	write_date, 
	active, 
	write_uid, 
	email,
	journal_id
) SELECT
	agofer.id, 
	agofer.city, 
	agofer.create_date, 
	agofer.name, 
	agofer.zip, 
	agofer.create_uid, 
	agofer.country, 
	agofer.street2, 
	agofer.bic, 
	agofer.phone, 
	agofer.state, 
	agofer.street, 
	agofer.write_date, 
	agofer.active, 
	agofer.write_uid, 
	agofer.email,
	--agofer.journal_id
	null
FROM dblink('dbname=agofer_08','select
	id, 
	city, 
	create_date, 
	name, 
	zip, 
	create_uid, 
	country, 
	street2, 
	bic, 
	phone, 
	state, 
	street, 
	write_date, 
	active, 
	write_uid, 
	email
	from res_bank;'
) AS agofer(
	id integer, 
	city character varying, 
	create_date timestamp without time zone, 
	name character varying, 
	zip character varying, 
	create_uid integer, 
	country integer, 
	street2 character varying, 
	bic character varying, 
	phone character varying, 
	state integer, 
	street character varying, 
	write_date timestamp without time zone, 
	active boolean, 
	write_uid integer, 
	email character varying
);

select setval('res_bank_id_seq', (select max(id) from res_bank));