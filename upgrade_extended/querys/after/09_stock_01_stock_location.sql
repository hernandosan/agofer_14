ALTER TABLE stock_location DISABLE TRIGGER ALL;

delete from stock_location as sl
using dblink('dbname=agofer_08','select id from stock_location;') as agofer (id integer) 
where sl.id = agofer.id;

ALTER TABLE stock_location ENABLE TRIGGER ALL;

INSERT INTO stock_location (
	id, 
	comment, 
	create_date, 
	write_date, 
	create_uid, 
	write_uid, 
	posz, 
	posx, 
	posy,
	active, 
	removal_strategy_id, 
	scrap_location, 
	name, 
	location_id, 
	company_id, 
	complete_name, 
	usage, 
	valuation_in_account_id, 
	valuation_out_account_id
) SELECT
	agofer.id, 
	agofer.comment, 
	agofer.create_date, 
	agofer.write_date, 
	agofer.create_uid, 
	agofer.write_uid, 
	agofer.posz, 
	agofer.posx, 
	agofer.posy, 
	agofer.active, 
	agofer.removal_strategy_id, 
	agofer.scrap_location, 
	agofer.name, 
	agofer.location_id, 
	-- agofer.company_id, 
	1, 
	agofer.complete_name, 
	agofer.usage, 
	agofer.valuation_in_account_id, 
	agofer.valuation_out_account_id
FROM dblink('dbname=agofer_08', 'select
	id, 
	comment, 
	create_date, 
	write_date, 
	create_uid, 
	write_uid, 
	posz, 
	posx, 
	posy, 
	active, 
	removal_strategy_id, 
	scrap_location, 
	name, 
	location_id, 
	company_id, 
	complete_name, 
	usage, 
	valuation_in_account_id, 
	valuation_out_account_id
	from stock_location;'
) AS agofer(
	id integer, 
	comment text, 
	create_date timestamp without time zone, 
	write_date timestamp without time zone, 
	create_uid integer, 
	write_uid integer, 
	posz integer, 
	posx integer, 
	posy integer, 
	active boolean, 
	removal_strategy_id integer,
	scrap_location boolean, 
	name character varying, 
	location_id integer, 
	company_id integer, 
	complete_name character varying, 
	usage character varying, 
	valuation_in_account_id integer, 
	valuation_out_account_id integer
);

select setval('stock_location_id_seq', (select max(id) from stock_location));

update ir_model_data imd 
set res_id = agofer.res_id 
from dblink('dbname=agofer_08','select name, model, res_id from ir_model_data where model = ''stock.location'';') as agofer 
(name character varying, model character varying, res_id integer) 
where agofer.name = imd.name 
and imd.model = 'stock.location';