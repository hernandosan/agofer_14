--SELECT column_name, data_type FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'product_product';

insert into product_product (id, 
create_uid, 
create_date, 
write_uid, 
default_code, 
write_date, 
active, 
product_tmpl_id)
select agofer.id, 
agofer.create_uid, 
agofer.create_date, 
agofer.write_uid, 
agofer.default_code, 
agofer.write_date, 
agofer.active, 
agofer.product_tmpl_id 
from dblink('dbname=agofer_08',
            'select id, 
create_uid, 
create_date, 
write_uid, 
default_code, 
write_date, 
active, 
product_tmpl_id
from product_product;') as agofer(id integer, 
create_uid integer, 
create_date timestamp without time zone, 
write_uid integer, 
default_code character varying, 
write_date timestamp without time zone, 
active boolean, 
product_tmpl_id integer)
where agofer.id not in (select id from product_product);

select setval('product_product_id_seq', (select max(id) from product_product));
