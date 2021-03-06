INSERT INTO res_users (
	id, 
	active, 
	login, 
	password, 
	company_id, 
	partner_id, 
	create_date, 
	create_uid, 
	write_uid, 
	write_date, 
	signature, 
	action_id, 
	share, 
	oauth_access_token,
	oauth_access_max_token,
	oauth_uid, 
	oauth_provider_id, 
	notification_type,
	oauth_master_uuid
	-- tz
) SELECT
	agofer.id, 
	agofer.active, 
	agofer.login, 
	agofer.password, 
	agofer.company_id, 
	agofer.partner_id, 
	agofer.create_date, 
	agofer.create_uid, 
	agofer.write_uid, 
	agofer.write_date, 
	agofer.signature, 
	agofer.action_id, 
	agofer.share, 
	agofer.oauth_access_token,
	agofer.oauth_access_max_token,
	agofer.oauth_uid, 
	agofer.oauth_provider_id,
	--agofer.notification_type
	'email',
	--agofer.oauth_master_uuid
	'null'
	-- 'America/Bogota'
FROM dblink('dbname=agofer_08', 'select
	id, 
	active, 
	login, 
	password, 
	company_id, 
	partner_id, 
	create_date, 
	create_uid, 
	write_uid, 
	write_date, 
	signature, 
	action_id, 
	share, 
	oauth_access_token,
	oauth_uid,
	oauth_provider_id,
	oauth_access_max_token
	from res_users;'
) AS agofer (
	id integer, 
	active boolean, 
	login character varying, 
	password character varying, 
	company_id integer, 
	partner_id integer, 
	create_date timestamp without time zone, 
	create_uid integer, 
	write_uid integer, 
	write_date timestamp without time zone, 
	signature text, 
	action_id integer, 
	share boolean, 
	oauth_access_token character varying, 
	oauth_uid character varying, 
	oauth_provider_id integer,
	oauth_access_max_token integer
)
WHERE agofer.id NOT IN (SELECT id FROM res_users);

select setval('res_users_id_seq', (select max(id) from res_users));