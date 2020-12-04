INSERT INTO res_partner_bank (
	id, 
	create_date, 
	sequence, 
	write_uid, 
	write_date, 
	partner_id, 
	company_id, 
	acc_number, 
	create_uid, 
	currency_id,
	bank_id,
	acc_holder_name,
	active
) SELECT
	agofer.id, 
	agofer.create_date, 
	agofer.sequence, 
	agofer.write_uid, 
	agofer.write_date, 
	agofer.partner_id, 
	agofer.company_id, 
	agofer.acc_number, 
	agofer.create_uid, 
	agofer.currency_id,
	agofer.bank,
	agofer.owner_name,
	--agofer.active
	TRUE
FROM dblink('dbname=agofer_08','select
	id, 
	create_date, 
	sequence, 
	write_uid, 
	write_date, 
	partner_id, 
	company_id, 
	acc_number, 
	create_uid, 
	currency_id,
	bank,
	owner_name
	from res_partner_bank;'
) AS agofer(
	id integer, 
	create_date timestamp without time zone, 
	sequence integer, 
	write_uid integer, 
	write_date timestamp without time zone, 
	partner_id integer, 
	company_id integer, 
	acc_number character varying, 
	create_uid integer, 
	currency_id integer,
	bank integer,
	owner_name character varying
);