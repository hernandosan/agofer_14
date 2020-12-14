INSERT INTO product_pricelist_item (
	id, 
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
	compute_price
) SELECT
	agofer.id, 
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
	agofer.base, 
	agofer.min_quantity, 
	agofer.price_min_margin, 
	agofer.categ_id, 
	agofer.price_surcharge,
	agofer.pricelist_id,
	'3_global',
	'fixed'
FROM dblink('dbname=agofer_08','select
	ppi.id, 
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
	pp.id as pricelist_id
from product_pricelist_item ppi
inner join product_pricelist_version ppv on ppv.id = ppi.price_version_id 
inner join product_pricelist pp on pp.id = ppv.pricelist_id
where ppv.date_end is null;'
) AS agofer(
	id integer, 
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
	pricelist_id integer
)
INNER JOIN product_pricelist PP ON PP.id = agofer.pricelist_id;

select setval('product_pricelist_item_id_seq', (select max(id) from product_pricelist_item));