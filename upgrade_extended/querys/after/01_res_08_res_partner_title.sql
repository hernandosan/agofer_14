INSERT INTO res_partner_title (name, schortcut) VALUES ('Corporacion', 'Corp.');

INSERT INTO res_partner_title (name, schortcut) VALUES ('Limitada', 'Ltda.');

INSERT INTO res_partner_title (name, schortcut) VALUES ('Sociedad por acciones simplificada', 'S.A.S.');

INSERT INTO res_partner_title (name, schortcut) VALUES ('Corporacion', 'Corp.');

INSERT INTO res_partner_title (name, schortcut) VALUES ('Doctora', 'Dra.');

INSERT INTO res_partner_title (name, schortcut) VALUES ('Señor', 'Sir.');

select setval('res_partner_title_id_seq', (select max(id) from res_partner_title));