insert into product_supplierinfo (product_name, 
create_uid, 
create_date, 
sequence, 
write_uid, 
write_date, 
company_id, 
currency_id, 
name, 
product_tmpl_id, 
product_id, 
min_qty,
price,
delay)
select cast(agofer.id as character varying), 
agofer.create_uid, 
agofer.create_date, 
agofer.sequence, 
agofer.write_uid, 
agofer.write_date, 
agofer.company_id, 
agofer.currency_id, 
agofer.name, 
agofer.product_tmpl_id, 
agofer.product_id, 
agofer.min_quantity, 
agofer.price_surcharge,
3
from dblink('dbname=agofer_08',
            'select ppi.id, 
pp.create_uid,
pp.create_date,
ppi.sequence,
pp.write_uid,
pp.write_date,
pp.company_id,
pp.currency_id,
cast(split_part(ip.res_id,'','',2) as integer) as name, 
ppi.product_tmpl_id,
ppi.product_id,
ppi.min_quantity, 
ppi.price_surcharge
from product_pricelist_item ppi 
inner join product_pricelist_version ppv on ppv.id = ppi.price_version_id
inner join product_pricelist pp on pp.id = ppv.pricelist_id
left join ir_property ip on cast(split_part(ip.value_reference,'','',2) as integer) = pp.id
where pp.type = ''purchase'' 
and ip.name = ''property_product_pricelist_purchase'' 
and ip.value_reference is not null 
and ip.res_id is not null;') as agofer(id integer, 
create_uid integer, 
create_date timestamp without time zone, 
sequence integer, 
write_uid integer, 
write_date timestamp without time zone, 
company_id integer, 
currency_id integer, 
name integer, 
product_tmpl_id integer, 
product_id integer,
min_quantity integer, 
price_surcharge numeric);