INSERT INTO calendar_event (
    id,
    allday,
    create_date,
    write_date,
    recurrency,
    write_uid,
    duration,
    stop_date,
    create_uid,
    user_id,
    start,
    location,
    start_date,
    description,
    stop,
    active,
    name,
    show_as,
    opportunity_id,
    recurrence_id
) SELECT
    agofer.id,
    agofer.allday,
    agofer.create_date,
    agofer.write_date,
    agofer.recurrency,
    agofer.write_uid,
    agofer.duration,
    agofer.stop_date,
    agofer.create_uid,
    agofer.user_id,
    agofer.start,
    agofer.location,
    agofer.start_date,
    agofer.description,
    agofer.stop,
    agofer.active,
    agofer.name,
    agofer.show_as,
    agofer.opportunity_id,
    agofer.recurrent_id
FROM dblink('dbname=agofer_08', 'select
        id,
        allday,
        create_date,
        write_date,
        recurrency,
        write_uid,
        duration,
        stop_date,
        create_uid,
        user_id,
        start,
        location,
        start_date,
        description,
        stop,
        active,
        name,
        show_as,
        opportunity_id,
        recurrent_id
        from calendar_event;'
) AS agofer(
    id integer,
    allday boolean,
    create_date timestamp without time zone,
    write_date timestamp without time zone,
    recurrency boolean,
    write_uid integer,
    duration double precision,
    stop_date date,
    create_uid integer,
    user_id integer,
    start timestamp without time zone,
    location character varying,
    start_date date,
    description text,
    stop timestamp without time zone,
    active boolean,
    name character varying,
    show_as character varying,
    opportunity_id integer,
    recurrent_id integer
);

SELECT setval('calendar_event_id_seq', (SELECT max(id) FROM calendar_event));