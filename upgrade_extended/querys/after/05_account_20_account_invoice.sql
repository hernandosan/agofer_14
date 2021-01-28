update account_move as am 
set move_type = agofer.type, 
invoice_date = agofer.date_invoice, 
invoice_date_due = agofer.date_due, 
invoice_user_id = agofer.user_id, 
-- team_id = agofer.section_id, 
invoice_partner_display_name = agofer.display_name, 
amount_total = agofer.amount_total, 
amount_residual = agofer.residual, 
amount_untaxed_signed = case when agofer.type in ('in_invoice', 'out_refund') then - agofer.amount_tax else agofer.amount_tax end, 
amount_total_signed = case when agofer.type in ('in_invoice', 'out_refund') then - agofer.amount_total else agofer.amount_total end, 
payment_state = case 
	when agofer.state = 'paid' then 'paid' 
	when agofer.state = 'open' and agofer.residual > 0 then 'partial'
	else 'not_paid' 
end 
from dblink('dbname=agofer_08','select ai.id, 
ai.type, 
ai.move_id, 
ai.date_invoice, 
ai.date_due, 
ai.amount_total, 
ai.amount_tax, 
ai.residual, 
ai.user_id, 
ai.section_id, 
ai.state, 
rp.display_name 
from account_invoice ai 
inner join res_partner rp on rp.id = ai.partner_id') as agofer 
(id integer, 
 type character varying, 
 move_id integer, 
 date_invoice date, 
 date_due date, 
 amount_total numeric, 
 amount_tax numeric, 
 residual numeric, 
 user_id integer, 
 section_id integer, 
 state character varying, 
 display_name character varying) 
where am.id = agofer.move_id;