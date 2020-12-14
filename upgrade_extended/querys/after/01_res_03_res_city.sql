INSERT INTO res_city (
	id, 
	name, 
	zipcode, 
	country_id, 
	state_id, 
	create_uid, 
	create_date, 
	write_uid, 
	write_date
) SELECT
    agofer.id,
	agofer.name, 
	agofer.zipcode, 
	agofer.country_id, 
	agofer.state_id,
	--agofer.create_uid
	2,
	agofer.create_date,
	--agofer.write_uid
	2,
	agofer.write_date 
FROM dblink('dbname=agofer_08', 'select
	city.id AS id,
	city.name AS name,
	city.code AS zipcode,
	country.id AS country_id,
	state.id AS state_id,
	city.create_uid,
	city.create_date,
	city.write_uid,
	city.write_date
	FROM res_city city
	INNER JOIN res_country_state state ON state.id = city.provincia_id
	INNER JOIN res_country country ON country.id = state.country_id
	ORDER BY city.id,
	city.name,
	city.code,
	country.id,
	state.id,
	city.create_uid,
	city.create_date,
	city.write_uid,
	city.write_date;'
) AS agofer(
	id integer, 
	name character varying, 
	zipcode character varying, 
	country_id integer, 
	state_id integer, 
	create_uid integer, 
	create_date timestamp without time zone, 
	write_uid integer, 
	write_date timestamp without time zone
)
WHERE agofer.id NOT IN (SELECT id FROM res_city);

select setval('res_city_id_seq', (select max(id) from res_city));

update res_city as rc
set state_id = rcs.id, country_id = rco.id
from dblink('dbname=agofer_08','select rc.id as id, rc.name as name, rcs.id as id2, rcs.name as name2, rco.code
from res_city rc
inner join res_country_state rcs on rcs.id = rc.provincia_id
inner join res_country rco on rco.id = rcs.country_id
order by rc.id, rcs.id;') as agofer (id integer, name character varying, id2 integer, name2 character varying, code character varying)
inner join res_country_state rcs on rcs.name = agofer.name2
inner join res_country rco on rco.code = agofer.code
where agofer.id = rc.id;