insert into account_group (name, company_id, niif_bool) 
select left(code, -2), 1, False from account_account group by left(code, -2);

insert into account_group (name, company_id, niif_bool) 
select left(code, -4), 1, False from account_account group by left(code, -4);

insert into account_group (name, company_id, niif_bool) 
select left(code, -6), 1, False from account_account group by left(code, -6);

insert into account_group (name, company_id, niif_bool) 
select left(code, -8), 1, False from account_account group by left(code, -8);

insert into account_group (name, company_id, niif_bool) 
select left(code, -10), 1, False from account_account group by left(code, -10);

delete from account_group where name = '';

update account_group as ag 
set parent_id = ag2.id
from account_group ag2 
where ag2.name = left(ag.name, 2)
and length(ag.name) = 4;

update account_group as ag 
set parent_id = ag2.id
from account_group ag2 
where ag2.name = left(ag.name, 4)
and length(ag.name) = 6;

update account_group as ag 
set parent_id = ag2.id
from account_group ag2 
where ag2.name = left(ag.name, 6)
and length(ag.name) = 8;

update account_account as aa
set group_id = ag.id
from account_group ag 
where ag.name = left(aa.code, 4) 
and length(aa.code) = 6;

update account_account as aa
set group_id = ag.id
from account_group ag 
where ag.name = left(aa.code, 6) 
and length(aa.code) = 8;

update account_account as aa
set group_id = ag.id
from account_group ag 
where ag.name = left(aa.code, 8) 
and length(aa.code) = 10;

update account_group as ag 
set code_prefix_start = aa.min,
code_prefix_end = aa.max
from (select ag.id, lpad(cast(min(cast(right(aa.code, 2) as integer)) as character varying), 2, '0') as min, 
lpad(cast(max(cast(right(aa.code, 2) as integer)) as character varying), 2, '0') as max
from account_group ag 
inner join account_account aa on aa.group_id = ag.id 
group by ag.id) as aa 
where aa.id = ag.id;

update mail_alias ma 
set alias_name = agofer.alias_name
from dblink('dbname=agofer_08','SELECT id, alias_name FROM mail_alias;') as agofer (id integer, alias_name character varying)
where agofer.id = ma.id 
and ma.alias_name != agofer.alias_name;

update hr_job hj 
set alias_id = agofer.alias_id
from dblink('dbname=agofer_08','SELECT id, alias_id FROM hr_job;') as agofer (id integer, alias_id integer) 
inner join mail_alias ma on ma.id = agofer.alias_id
where agofer.id = hj.id and hj.alias_id != agofer.alias_id;

update hr_employee he 
set resource_id = agofer.resource_id
from dblink('dbname=agofer_08','SELECT id, resource_id FROM hr_employee;') as agofer (id integer, resource_id integer) 
inner join resource_resource rr on rr.id = agofer.resource_id
where agofer.id = he.id and he.resource_id != agofer.resource_id;

update ir_sequence ise 
set prefix = agofer.prefix,
suffix = agofer.suffix,
padding = agofer.padding,
number_next = agofer.number_next
from dblink('dbname=agofer_08','SELECT id, code, prefix, suffix, padding, number_next FROM ir_sequence;') as agofer 
(id integer, code character varying, prefix character varying, suffix character varying, padding integer, number_next integer) 
where agofer.id = ise.id;

update ir_sequence ise
set prefix = agofer.prefix,
suffix = agofer.suffix,
padding = agofer.padding,
number_next = agofer.number_next
from dblink('dbname=agofer_08','SELECT id, code, prefix, suffix, padding, number_next FROM ir_sequence;') as agofer
(id integer, code character varying, prefix character varying, suffix character varying, padding integer, number_next integer)
where agofer.code = ise.code;

update product_category set parent_path = '' where parent_path is null;

update product_category set parent_path = cast(id as character varying) || '/' where parent_path = '' and parent_id is null;

update stock_location set parent_path = '' where parent_path is null;

update stock_location set parent_path = cast(id as character varying) || '/' where parent_path = '' and location_id is null;

update account_account aa
set code = agofer.code
from dblink('dbname=agofer_08','SELECT id, code FROM account_account;') as agofer
(id integer, code character varying)
where agofer.id = aa.id;

update account_move_line aml
set statement_id = agofer.statement_id
from dblink('dbname=agofer_08','SELECT id, statement_id FROM account_move_line;') as agofer
(id integer, statement_id integer)
inner join account_bank_statement abs on agofer.statement_id = abs.id
where agofer.id = aml.id;

update account_move_line aml
set statement_line_id = agofer.statement_line_id
from dblink('dbname=agofer_08','SELECT id, statement_line_id FROM account_move_line;') as agofer
(id integer, statement_id integer)
inner join account_bank_statement_line abs on agofer.statement_line_id = abs.id
where agofer.id = aml.id;

update res_partner rp
set write_uid = agofer.write_uid,
create_uid = agofer.create_uid
from dblink('dbname=agofer_08','SELECT id, write_uid, create_uid FROM res_partner;') as agofer (id integer, write_uid integer, create_uid integer)
where agofer.id = rp.id;

update stock_quant as sq
set quantity = agofer.qty,
reserved_quantity = 0.0
from dblink('dbname=agofer_08','select id, qty from stock_quant;') AS agofer (id integer, qty double precision)
where agofer.id = sq.id;