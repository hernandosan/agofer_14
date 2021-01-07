INSERT INTO ir_attachment (
    id,
    create_uid,
    create_date,
    description,
    url,
    res_model,
    company_id,
    write_uid,
    type,
    res_id,
    write_date,
    file_size,
    db_datas,
    store_fname,
    name,
    mimetype,
    index_content
) SELECT
    agofer.id,
    agofer.create_uid,
    agofer.create_date,
    agofer.description,
    agofer.url,
    agofer.res_model,
    agofer.company_id,
    agofer.write_uid,
    agofer.type,
    agofer.res_id,
    agofer.write_date,
    agofer.file_size,
    agofer.db_datas,
    agofer.store_fname,
    agofer.name,
    agofer.mimetype,
    agofer.index_content
FROM dblink('dbname=agofer_08', 'select
    id,
    create_uid,
    create_date,
    description,
    url,
    res_model,
    company_id,
    write_uid,
    type,
    res_id,
    write_date,
    file_size,
    db_datas,
    store_fname,
    name,
    mimetype,
    index_content
    from ir_attachment;'
) AS agofer (
    id integer,
    create_uid integer,
    create_date timestamp without time zone,
    description text,
    url character varying,
    res_model character varying,
    company_id integer,
    write_uid integer,
    type character varying,
    res_id integer,
    write_date timestamp without time zone,
    file_size integer,
    db_datas bytea,
    store_fname character varying,
    name character varying,
    mimetype character varying,
    index_content text
<<<<<<< HEAD
)
WHERE agofer.id NOT IN (SELECT id FROM ir_attachment);;
=======
) inner join ir_model im on im.model = agofer.res_model 
where agofer.id not in (select id from ir_attachment);
>>>>>>> 5b9791b2270fa8550f46f5362f5d832fddffed56

select setval('ir_attachment_id_seq', (select max(id) from ir_attachment));