insert into res_city (
	id, 
	name, 
	zipcode, 
	country_id, 
	state_id, 
	create_uid, 
	create_date, 
	write_uid, 
	write_date) 
	select agofer.id, 
	agofer.name, 
	agofer.zipcode, 
	agofer.country_id, 
	agofer.state_id,
	2, 
	agofer.create_date,
	2, 
	agofer.write_date 
from dblink('dbname=agofer_08', 'select 
	city.id as id,
	city.name as name,
	city.code as zipcode,
	country.id as country_id,
	state.id as state_id,
	city.create_uid,
	city.create_date,
	city.write_uid,
	city.write_date
	from res_city city
	inner join res_country_state state on state.id = city.provincia_id
	inner join res_country country on country.id = state.country_id 
	order by city.id,
	city.name,
	city.code,
	country.id,
	state.id,
	city.create_uid,
	city.create_date,
	city.write_uid,
	city.write_date;'
) as agofer(
	id integer, 
	name character varying, 
	zipcode character varying, 
	country_id integer, 
	state_id integer, 
	create_uid integer, 
	create_date timestamp without time zone, 
	write_uid integer, 
	write_date timestamp without time zone
)where agofer.id NOT IN (SELECT id FROM res_city);
