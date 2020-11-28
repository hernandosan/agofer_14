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
