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
	agofer.price_version_id,
	--agofer.applied_on
	'3_global',
	--agofer.compute_price
	'fixed'
FROM dblink('dbname=agofer_08','select
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
	price_version_id
	from product_pricelist_item;'
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
	price_version_id integer
)
INNER JOIN product_pricelist PP ON PP.id = agofer.price_version_id;



