insert into res_partner (
	id, 
	name,
	company_id,
	comment,
	create_date,
	color,
	active,
	street,
	user_id,
	zip,
	title,
	function,
	country_id,
	parent_id,
	employee,
	type,
	email,
	vat,
	website,
	lang,
	city,
	street2,
	phone,
	credit_limit,
	write_date,
	date,
	tz,
	write_uid,
	display_name,
	create_uid,
	mobile,
	ref,
	is_company,
	state_id,
	commercial_partner_id,
	signup_type,
	signup_expiration,
	signup_token,
	debit_limit,
	city_id,
	calendar_last_notif_ack,
	picking_warn,
	sale_warn,
	purchase_warn,
	invoice_warn_msg,
	picking_warn_msg,
	invoice_warn,
	purchase_warn_msg,
	sale_warn_msg
)select 
	agofer.id, 
	agofer.name, 
	agofer.company_id, 
	agofer.comment, 
	agofer.create_date, 
	agofer.color, 
	agofer.active, 
	agofer.street, 
	--agofer.user_id,
	2,
	agofer.zip, 
	agofer.title, 
	agofer.function, 
	agofer.country_id, 
	agofer.parent_id, 
	agofer.employee, 
	agofer.type, 
	agofer.email, 
	agofer.vat, 
	agofer.website, 
	agofer.lang, 
	agofer.city, 
	agofer.street2, 
	agofer.phone, 
	agofer.credit_limit, 
	agofer.write_date, 
	agofer.date, 
	agofer.tz, 
	--agofer.write_uid, 
	2,
	agofer.display_name, 
	--agofer.create_uid,
	2,
	agofer.mobile, 
	agofer.ref, 
	agofer.is_company, 
	agofer.state_id, 
	agofer.commercial_partner_id, 
	agofer.signup_type, 
	agofer.signup_expiration, 
	agofer.signup_token, 
	agofer.debit_limit, 
	agofer.city_id, 
	agofer.calendar_last_notif_ack, 
	agofer.picking_warn, 
	agofer.sale_warn, 
	agofer.purchase_warn, 
	agofer.invoice_warn_msg, 
	agofer.picking_warn_msg, 
	agofer.invoice_warn, 
	agofer.purchase_warn_msg, 
	agofer.sale_warn_msg  
from dblink('dbname=agofer_08','select 
	id, 
	name, 
	company_id, 
	comment, 
	create_date, 
	color, 
	active, 
	street, 
	user_id, 
	zip, 
	title, 
	function, 
	country_id, 
	parent_id, 
	employee, 
	type, 
	email, 
	vat, 
	website, 
	lang, 
	city, 
	street2, 
	phone, 
	credit_limit, 
	write_date, 
	date, 
	tz, 
	write_uid, 
	display_name, 
	create_uid, 
	mobile, 
	ref, 
	is_company, 
	state_id, 
	commercial_partner_id, 
	signup_type, 
	signup_expiration, 
	signup_token, 
	debit_limit, 
	city_id, 
	calendar_last_notif_ack, 
	picking_warn, 
	sale_warn, 
	purchase_warn, 
	invoice_warn_msg, 
	picking_warn_msg, 
	invoice_warn, 
	purchase_warn_msg, 
	sale_warn_msg
	from res_partner;'
) as agofer(
	id integer, 
	name character varying, 
	company_id integer, 
	comment text, 
	create_date timestamp without time zone, 
	color integer, 
	active boolean, 
	street character varying, 
	user_id integer, 
	zip character varying, 
	title integer, 
	function character varying, 
	country_id integer, 
	parent_id integer, 
	employee boolean, 
	type character varying, 
	email character varying, 
	vat character varying, 
	website character varying, 
	lang character varying, 
	city character varying, 
	street2 character varying, 
	phone character varying, 
	credit_limit double precision, 
	write_date timestamp without time zone, 
	date date, 
	tz character varying, 
	write_uid integer, 
	display_name character varying, 
	create_uid integer, 
	mobile character varying, 
	ref character varying, 
	is_company boolean, 
	state_id integer, 
	commercial_partner_id integer, 
	signup_type character varying, 
	signup_expiration timestamp without time zone, 
	signup_token character varying, 
	debit_limit double precision, 
	city_id integer, 
	calendar_last_notif_ack timestamp without time zone, 
	picking_warn character varying, 
	sale_warn character varying, 
	purchase_warn character varying, 
	invoice_warn_msg text, 
	picking_warn_msg text, 
	invoice_warn character varying, 
	purchase_warn_msg text, 
	sale_warn_msg text
)where agofer.id not in (select id from res_partner);
