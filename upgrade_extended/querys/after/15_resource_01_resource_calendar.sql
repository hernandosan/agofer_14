UPDATE resource_calendar 
SET create_uid = agofer.create_uid,
	create_date = agofer.create_date, 
	name = agofer.name,
	company_id = agofer.company_id,
	write_uid = agofer.write_uid,
	write_date = agofer.write_date, 
	tz = agofer.tz
FROM
	(select 
		agofer.id, 
		agofer.create_uid, 
		agofer.create_date, 
		agofer.name, 
		agofer.company_id, 
		agofer.write_uid, 
		agofer.write_date, 
		agofer.tz
		from dblink('dbname=agofer_08','SELECT 
			id, 
			create_uid, 
			create_date, 
			name, 
			company_id, 
			write_uid, 
			write_date, 
			tz
			FROM resource_calendar;'
		) as agofer(
			id integer, 
			create_uid integer, 
			create_date timestamp without time zone, 
			name character varying, 
			company_id integer, 
			write_uid integer, 
			write_date timestamp without time zone, 
			tz character varying
	))as agofer 
WHERE resource_calendar.id = agofer.id;