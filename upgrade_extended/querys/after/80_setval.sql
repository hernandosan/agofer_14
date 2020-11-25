select setval('res_country_id_seq', (select max(id) from res_country));

select setval('res_city_id_seq', (select max(id) from res_city));

select setval('res_partner_id_seq', (select max(id) from res_partner));

select setval('res_users_id_seq', (select max(id) from res_users));

select setval('ir_sequence_id_seq', (select max(id) from ir_sequence));

select setval('mail_message_id_seq', (select max(id) from mail_message));

select setval('product_category_id_seq', (select max(id) from product_category));

select setval('uom_category_id_seq', (select max(id) from uom_category));

select setval('uom_uom_id_seq', (select max(id) from uom_uom));

select setval('product_template_id_seq', (select max(id) from product_template));

select setval('product_product_id_seq', (select max(id) from product_product));

select setval('product_pricelist_id_seq', (select max(id) from product_pricelist));

select setval('account_payment_term_id_seq', (select max(id) from account_payment_term));

select setval('account_journal_id_seq', (select max(id) from account_journal));

select setval('account_account_id_seq', (select max(id) from account_account));

select setval('account_move_id_seq', (select max(id) from account_move));

select setval('account_analytic_account_id_seq', (select max(id) from account_analytic_account));

select setval('account_move_line_id_seq', (select max(id) from account_move_line));

select setval('account_payment_mode_id_seq', (select max(id) from account_payment_mode));

select setval('account_payment_order_id_seq', (select max(id) from account_payment_order));

select setval('account_asset_profile_id_seq', (select max(id) from account_asset_profile));

select setval('account_asset_id_seq', (select max(id) from account_asset));

select setval('account_asset_line_id_seq', (select max(id) from account_asset_line));

select setval('account_tax_id_seq', (select max(id) from account_asset_tax));

select setval('procurement_group_id_seq', (select max(id) from procurement_group));

select setval('delivery_carrier_id_seq', (select max(id) from delivery_carrier));

select setval('stock_location_id_seq', (select max(id) from stock_location));

select setval('stock_location_route_id_seq', (select max(id) from stock_location_route));

select setval('stock_picking_type_id_seq', (select max(id) from stock_picking_type));

select setval('stock_rule_id_seq', (select max(id) from stock_rule));

select setval('stock_warehouse_id_seq', (select max(id) from stock_warehouse));

select setval('stock_picking_id_seq', (select max(id) from stock_picking));

select setval('stock_inventory_id_seq', (select max(id) from stock_inventory));

select setval('mrp_bom_id_seq', (select max(id) from mrp_bom));

select setval('mrp_production_id_seq', (select max(id) from mrp_production));

select setval('purchase_import_id_seq', (select max(id) from purchase_import));

select setval('purchase_order_id_seq', (select max(id) from purchase_order));

select setval('purchase_order_line_id_seq', (select max(id) from purchase_order_line));

select setval('stock_move_id_seq', (select max(id) from stock_move));

select setval('sale_order_id_seq', (select max(id) from sale_order));

select setval('sale_order_line_id_seq', (select max(id) from sale_order_line));

select setval('helpdesk_ticket_team_id_seq', (select max(id) from helpdesk_ticket_team));

select setval('helpdesk_ticket_category_id_seq', (select max(id) from helpdesk_ticket_category));

select setval('helpdesk_ticket_id_seq', (select max(id) from helpdesk_ticket));
