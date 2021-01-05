--Update res_currency
update res_currency rc
set write_uid = agofer.write_uid,
create_uid = agofer.create_uid
from dblink('dbname=agofer_08','select id, write_uid, create_uid from res_currency;') as agofer (id integer, write_uid integer, create_uid integer)
where agofer.id = rc.id;

--Update res_country
update res_country rc
set write_uid = agofer.write_uid,
create_uid = agofer.create_uid
from dblink('dbname=agofer_08','select id, write_uid, create_uid from res_country;') as agofer (id integer, write_uid integer, create_uid integer)
where agofer.id = rc.id;

--Update res_country_state
update res_country_state rcs
set write_uid = agofer.write_uid,
create_uid = agofer.create_uid
from dblink('dbname=agofer_08','select id, write_uid, create_uid from res_country_state;') as agofer (id integer, write_uid integer, create_uid integer)
where agofer.id = rcs.id;

--Update res_city
update res_city rc
set write_uid = agofer.write_uid,
create_uid = agofer.create_uid
from dblink('dbname=agofer_08','select id, write_uid, create_uid from res_city;') as agofer (id integer, write_uid integer, create_uid integer)
where agofer.id = rc.id;

--Update res_partner
update res_partner rp
set write_uid = agofer.write_uid,
create_uid = agofer.create_uid,
user_id = agofer.user_id,
payment_responsible_id = agofer.user_id
from dblink('dbname=agofer_08','select id, write_uid, create_uid, user_id from res_partner;') as agofer (id integer, write_uid integer, create_uid integer, user_id integer)
where agofer.id = rp.id;

update res_partner set credit_control = True, credit_type = 'insured' where credit_limit > 0 and parent_id is null;

--Update product_category
update product_category set parent_path = '' where parent_path is null;

update product_category set parent_path = cast(id as character varying) || '/' where parent_path = '' and parent_id is null;

--Update stock_picking_type
update stock_picking_type spt
set warehouse_id = agofer.warehouse_id
from dblink('dbname=agofer_08','SELECT id, warehouse_id FROM stock_picking_type;')
as agofer (id integer, warehouse_id integer)
where agofer.id = spt.id;

--Update stock_rule
update stock_rule sr
set warehouse_id = agofer.warehouse_id
from dblink('dbname=agofer_08','SELECT id, warehouse_id FROM procurement_rule;')
as agofer (id integer, warehouse_id integer)
where agofer.id = sr.id;

--Update stock_picking
update stock_picking sp
set sale_id = agofer.sale_id,
backorder_id = agofer.backorder_id
from dblink('dbname=agofer_08','select id, sale_id, backorder_id from stock_picking;')
as agofer (id integer, sale_id integer, backorder_id integer)
where agofer.id = sp.id;

update stock_picking as sp
set location_id = sm.location_id,
location_dest_id = sm.location_dest_id
from stock_move sm
where sm.picking_id = sp.id;

update stock_picking set scheduled_date = date where scheduled_date is null;

update stock_picking set shipping_type = null where order_id is null;

update stock_picking as sp
set shipping_type = null
from stock_picking_type spt
where spt.id = sp.picking_type_id
and spt.code != 'outgoing'
and sp.shipping_type is not null;

update stock_picking set delivery_bool = True where shipping_type = 'delivery' and delivery_date is null;

update stock_picking set delivery_bool = True where shipping_type = 'pick' and pick_date is null;

--Update hr_department
update hr_department hd
set manager_id = agofer.manager_id
from dblink('dbname=agofer_08','select id, manager_id from hr_department;')
as agofer (id integer, manager_id integer)
where agofer.id = hd.id;

-- Update hr_job
update hr_job hj
set manager_id = agofer.manager_id
from dblink('dbname=agofer_08','select id, manager_id from hr_job;')
as agofer (id integer, manager_id integer)
where agofer.id = hj.id;

--Update hr_novelty
update hr_novelty set state = 'paid' where state = 'done';
update hr_novelty set state = 'cancel' where state in ('cancelled', 'refused');

--Update hr_overtime
update hr_overtime set state = 'cancel' where state in ('cancelled','refuse');