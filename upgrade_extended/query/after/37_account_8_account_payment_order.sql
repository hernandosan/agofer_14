insert into account_payment_order (
	id, 
	create_uid, 
	date_prefered, 
	date_done, 
	company_id, 
	write_uid, 
	state, 
	date_scheduled, 
	create_date,
	payment_mode_id,
	payment_type
)select 
	agofer.id, 
	agofer.create_uid, 
	agofer.date_prefered, 
	agofer.date_done, 
	agofer.company_id, 
	agofer.write_uid, 
	agofer.state, 
	agofer.date_scheduled, 
	agofer.create_date,
	agofer.mode,
	--agofer.payment_type,
	'inbound'
from dblink('dbname=agofer_08','SELECT 
	id, 
	create_uid, 
	date_prefered, 
	date_done, 
	company_id, 
	write_uid, 
	state, 
	date_scheduled, 
	create_date,
	mode
	FROM payment_order;'
) as agofer(
	id integer, 
	create_uid integer, 
	date_prefered character varying, 
	date_done date, 
	company_id integer, 
	write_uid integer, 
	state character varying, 
	date_scheduled date, 
	create_date timestamp without time zone,
	mode integer
);

