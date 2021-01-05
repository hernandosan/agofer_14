insert into product_pricelist_item (id, 
create_uid, 
price_round, 
create_date, 
price_discount, 
base_pricelist_id, 
write_uid, 
price_max_margin, 
write_date, 
company_id, 
product_tmpl_id, 
product_id, 
base, 
min_quantity, 
price_min_margin, 
categ_id, 
price_surcharge, 
pricelist_id, 
applied_on, 
compute_price, 
active, 
fixed_price,
currency_id)
select agofer.id, 
agofer.create_uid, 
agofer.price_round, 
agofer.create_date, 
agofer.price_discount, 
agofer.base_pricelist_id, 
agofer.write_uid, 
agofer.price_max_margin, 
agofer.write_date, 
agofer.company_id, 
agofer.product_tmpl_id, 
agofer.product_id, 
--agofer.base, 
case 
when agofer.base = '1' then 'list_price' 
when agofer.base = '2' then 'standard_price' 
when agofer.base = '-1' then 'pricelist' 
else 'list_price' 
end, 
agofer.min_quantity, 
agofer.price_min_margin, 
agofer.categ_id, 
agofer.price_surcharge, 
agofer.pricelist_id, 
case 
when agofer.product_id is not null then '0_product_variant' 
when agofer.product_tmpl_id is not null then '1_product' 
when agofer.categ_id is not null then '2_product_category' 
else '3_global' 
end, 
case 
when agofer.base = '1' then 'fixed' 
when agofer.base = '2' then 'percentage' 
when agofer.base = '-1' then 'formula' 
else 'fixed' 
end, 
case 
when agofer.date_end is not null then False 
else True 
end, 
agofer.price_surcharge, 
agofer.currency_id
from dblink('dbname=agofer_08',
            'select ppi.id, 
ppi.create_uid, 
ppi.price_round, 
ppi.create_date, 
ppi.price_discount, 
ppi.base_pricelist_id, 
ppi.write_uid, 
ppi.price_max_margin, 
ppi.write_date, 
ppi.company_id, 
ppi.product_tmpl_id, 
ppi.product_id, 
ppi.base, 
ppi.min_quantity, 
ppi.price_min_margin, 
ppi.categ_id, 
ppi.price_surcharge,
pp.id as pricelist_id, 
ppv.date_end, 
pp.currency_id
from product_pricelist_item ppi 
inner join product_pricelist_version ppv on ppv.id = ppi.price_version_id
inner join product_pricelist pp on pp.id = ppv.pricelist_id
where pp.type = ''sale'';') as agofer(id integer, 
create_uid integer, 
price_round numeric, 
create_date timestamp without time zone, 
price_discount numeric, 
base_pricelist_id integer, 
write_uid integer, 
price_max_margin numeric, 
write_date timestamp without time zone, 
company_id integer, 
product_tmpl_id integer, 
product_id integer, 
base integer, 
min_quantity integer, 
price_min_margin numeric, 
categ_id integer, 
price_surcharge numeric, 
pricelist_id integer, 
date_end date, 
currency_id integer);

select setval('product_pricelist_item_id_seq', (select max(id) from product_pricelist_item));