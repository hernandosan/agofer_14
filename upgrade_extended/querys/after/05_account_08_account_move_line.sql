INSERT INTO account_move_line (
	id, 
	create_date, 
	statement_id, 
	journal_id, 
	currency_id, 
	company_currency_id, 
	date_maturity, 
	partner_id, 
	blocked, 
	analytic_account_id, 
	create_uid, 
	credit, 
	company_id, 
	debit, 
	ref, 
	account_id, 
	write_date, 
	date, 
	write_uid, 
	move_id, 
	name, 
	product_id, 
	product_uom_id, 
	amount_currency, 
	quantity, 
	statement_line_id, 
	exclude_from_invoice_tab, 
	reconciled
) SELECT
	agofer.id, 
	agofer.create_date, 
	agofer.statement_id,
	agofer.journal_id,
	agofer.currency_id,
	9,
	agofer.date_maturity,
	agofer.partner_id,
	agofer.blocked,
	agofer.analytic_account_id,
	agofer.create_uid,
	agofer.credit,
	agofer.company_id,
	agofer.debit,
	agofer.ref,
	agofer.account_id,
	agofer.write_date,
	agofer.date,
	agofer.write_uid,
	agofer.move_id,
	agofer.name,
	agofer.product_id,
	agofer.product_uom_id,
	agofer.amount_currency,
	agofer.quantity,
	agofer.statement_line_id,
	True,
	case when agofer.reconcile_id is not null then True else False end
FROM dblink('dbname=agofer_08','select
	id,
	create_date,
	statement_id,
	journal_id,
	currency_id,
	date_maturity,
	partner_id,
	blocked,
	analytic_account_id,
	create_uid,
	credit,
	company_id,
	debit,
	ref,
	account_id,
	write_date,
	date,
	write_uid,
	move_id,
	name,
	product_id,
	product_uom_id,
	(case
	when currency_id != 9 and debit - credit <= 0 then - abs(amount_currency)
	when currency_id != 9 and debit - credit >= 0 then abs(amount_currency)
	when currency_id = 9 and round(debit - credit - amount_currency, 2) != 0 then debit -credit
	else amount_currency
	end),
	quantity,
	statement_line_id, 
	reconcile_id
	from account_move_line;'
) AS agofer(
	id integer,
	create_date timestamp without time zone,
	statement_id integer,
	journal_id integer,
	currency_id integer,
	date_maturity date,
	partner_id integer,
	blocked boolean,
	analytic_account_id integer,
	create_uid integer,
	credit numeric,
	company_id integer,
	debit numeric,
	ref character varying,
	account_id integer,
	write_date timestamp without time zone,
	date date,
	write_uid integer,
	move_id integer,
	name character varying,
	product_id integer,
	product_uom_id integer,
	amount_currency numeric,
	quantity numeric,
	statement_line_id integer,
	reconcile_id integer
);

select setval('account_move_line_id_seq', (select max(id) from account_move_line));

update account_move_line as aml 
set amount_residual = agofer.sum
from dblink('dbname=agofer_08','select aml.id, 
case
	when aml.reconcile_id is not null then 0.0 
	when aa.reconcile != True then 0.0 
	when aml.reconcile_partial_id is not null then abs(amr.sum)
	else abs(aml.debit - aml.credit)
end 
from account_move_line aml 
inner join account_account aa on aa.id = aml.account_id 
left join (select aml.id, sum(aml2.debit - aml2.credit)
from account_move_line aml
inner join account_move_reconcile amr on amr.id = aml.reconcile_partial_id 
inner join account_move_line aml2 on aml2.reconcile_partial_id = amr.id or aml2.reconcile_id = amr.id
where aml.id != aml2.id 
group by aml.id) amr on amr.id = aml.id') agofer (id integer, sum numeric) 
where aml.id = agofer.id;