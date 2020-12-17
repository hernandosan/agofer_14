INSERT INTO account_payment_term (name, active, note, sequence) VALUES ('40 Days', TRUE, 'Payment terms: 40 Days', 10);

INSERT INTO account_payment_term (name, active, note, sequence) VALUES ('Prepaid', TRUE, 'Total advance payment', 10);

INSERT INTO account_payment_term (name, active, note, sequence) VALUES ('3 Months', TRUE, 'Payment terms: 3 Months', 10);

INSERT INTO account_payment_term (name, active, note, sequence) VALUES ('Quota withdrawn', TRUE, 'Payments pending quota withdrawn by payment', 10);

INSERT INTO account_payment_term (name, active, note, sequence) VALUES ('120 Days', TRUE, 'Payment terms: 120 Days', 10);

INSERT INTO account_payment_term (name, active, note, sequence) VALUES ('Data update', TRUE, 'Quota suspended due to lack of use. Update documents', 10);

INSERT INTO account_payment_term (name, active, note, sequence) VALUES ('Quota canceled', TRUE, 'Quota canceled', 10);

INSERT INTO account_payment_term (name, active, note, sequence) VALUES ('7 Days', TRUE, 'Payment for providers only', 10);

INSERT INTO account_payment_term (name, active, note, sequence) VALUES ('8 Days', TRUE, 'Payment terms: 8 Days', 10);

INSERT INTO account_payment_term (name, active, note, sequence) VALUES ('75 Days', TRUE, 'Payment terms: 75 Days', 10);

select setval('account_payment_term_id_seq', (select max(id) from account_payment_term));