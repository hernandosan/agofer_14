INSERT INTO res_partner (
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
	sale_warn_msg,
    payment_next_action_date,
    payment_next_action,
    payment_note,
    payment_responsible_id,
    first_name,
    second_name,
    first_surname,
    second_surname,
    ref_num,
    verification_code,
    employee2emergency_id,
    ref_type_required,
    legal_status_type,
    eps,
    arl,
    afp,
    ccf,
    eps_code,
    arl_code,
    afp_code,
    ccf_code,
    ref_type_id,
	credit_control,
	credit_type
) SELECT
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
	agofer.sale_warn_msg,
	agofer.payment_next_action_date,
    agofer.payment_next_action,
    agofer.payment_note,
    --agofer.payment_responsible_id,
	3,
	agofer.primer_nombre,
	agofer.otros_nombres,
	agofer.primer_apellido,
	agofer.segundo_apellido,
	agofer.ref,
	agofer.dev_ref,
	--agofer.employee2emergency_id,
	null,
	--agofer.ref_type_required,
	FALSE,
	--agofer.legal_status_type,
	 'natural',
	agofer.eps,
	agofer.arl,
	agofer.afp,
	agofer.cajacomp,
	agofer.codigo_eps,
	agofer.codigo_arl,
	agofer.codigo_afp,
	agofer.codigo_ccf,
	--agofer.ref_type_id
	(case when agofer.ref_type = 2 then 1
	     when agofer.ref_type in (7,3,9, 10, 8, 4, null) then agofer.ref_type
         when agofer.ref_type = 1 then 2
         when agofer.ref_type = 6 then 5
         when agofer.ref_type = 5 then 6
         else null
    end),
	case when agofer.credit_limit > 0 and agofer.parent_id is null then True else False end,
	case when agofer.credit_limit > 0 and agofer.parent_id is null then 'insured' else null end
FROM dblink('dbname=agofer_08','select
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
	sale_warn_msg,
	payment_next_action_date,
    payment_next_action,
    payment_note,
    payment_responsible_id,
    primer_nombre,
    otros_nombres,
    primer_apellido,
    segundo_apellido,
	eps,
	arl,
	afp,
	cajacomp,
    codigo_eps,
    codigo_arl,
	codigo_afp,
	codigo_ccf,
    ref_type,
    dev_ref
	from res_partner;'
) AS agofer(
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
	sale_warn_msg text,
	payment_next_action_date date,
    payment_next_action text,
    payment_note text,
    payment_responsible_id integer,
    primer_nombre character varying,
    otros_nombres character varying,
    primer_apellido character varying,
    segundo_apellido character varying,
    eps boolean,
    arl boolean,
    afp boolean,
    cajacomp boolean,
    codigo_eps character varying,
    codigo_arl character varying,
    codigo_afp character varying,
    codigo_ccf character varying,
    ref_type integer,
    dev_ref	integer
)
WHERE agofer.id NOT IN (SELECT id FROM res_partner);

select setval('res_partner_id_seq', (select max(id) from res_partner));