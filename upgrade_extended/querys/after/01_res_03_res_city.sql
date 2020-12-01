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