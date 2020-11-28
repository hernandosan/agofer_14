insert into sale_order (
	id, 
	origin, 
	create_date, 
	write_uid, 
	client_order_ref, 
	date_order, 
	partner_id, 
	amount_tax, 
	procurement_group_id, 
	amount_untaxed, 
	company_id, 
	note, 
	state, 
	pricelist_id, 
	create_uid, 
	write_date, 
	partner_invoice_id, 
	user_id, 
	amount_total, 
	name, 
	partner_shipping_id, 
	picking_policy, 
	incoterm, 
	warehouse_id, 
	carrier_id, 
	validity_date, 
	access_token, 
	medium_id, 
	campaign_id, 
	source_id
) select 
	agofer.id, 
	agofer.origin, 
	agofer.create_date, 
	agofer.write_uid, 
	agofer.client_order_ref, 
	agofer.date_order, 
	agofer.partner_id, 
	agofer.amount_tax, 
	agofer.procurement_group_id, 
	agofer.amount_untaxed, 
	agofer.company_id, 
	agofer.note, 
	agofer.state, 
	agofer.pricelist_id, 
	agofer.create_uid, 
	agofer.write_date, 
	agofer.partner_invoice_id, 
	--agofer.user_id, 
	2, 
	agofer.amount_total, 
	agofer.name, 
	agofer.partner_shipping_id, 
	agofer.picking_policy, 
	agofer.incoterm, 
	agofer.warehouse_id, 
	agofer.carrier_id, 
	agofer.validity_date, 
	agofer.access_token, 
	agofer.medium_id, 
	agofer.campaign_id, 
	agofer.source_id 
from dblink('dbname=agofer_08', 'select 
	id, 
	origin, 
	create_date, 
	write_uid, 
	client_order_ref, 
	date_order, 
	partner_id, 
	amount_tax, 
	procurement_group_id, 
	amount_untaxed, 
	company_id, 
	note, 
	state, 
	pricelist_id, 
	create_uid, 
	write_date, 
	partner_invoice_id, 
	user_id, 
	amount_total, 
	name, 
	partner_shipping_id, 
	picking_policy, 
	incoterm, 
	warehouse_id, 
	carrier_id, 
	validity_date, 
	access_token, 
	medium_id, 
	campaign_id, 
	source_id
	from sale_order;'
) as agofer (
	id integer, 
	origin character varying, 
	create_date timestamp without time zone, 
	write_uid integer, 
	client_order_ref character varying, 
	date_order timestamp without time zone, 
	partner_id integer, 
	amount_tax numeric, 
	procurement_group_id integer, 
	amount_untaxed numeric, 
	company_id integer, 
	note text, 
	state character varying, 
	pricelist_id integer, 
	create_uid integer, 
	write_date timestamp without time zone, 
	partner_invoice_id integer, 
	user_id integer, 
	amount_total numeric, 
	name character varying, 
	partner_shipping_id integer, 
	picking_policy character varying, 
	incoterm integer, 
	warehouse_id integer, 
	carrier_id integer, 
	validity_date date, 
	access_token character varying, 
	medium_id integer, 
	campaign_id integer, 
	source_id integer
) 
where cast(agofer.date_order as date) >= '2019-01-01';