INSERT INTO uom_uom (active, uom_type, name, rounding, factor, category_id)
VALUES (TRUE, 'reference', 'Caja', 1.0, 1.0, 1);
INSERT INTO uom_uom (active, uom_type, name, rounding, factor, category_id)
VALUES (TRUE, 'reference', 'm²', 1.0, 1.0, 6);
INSERT INTO uom_uom (active, uom_type, name, rounding, factor, category_id)
VALUES (TRUE, 'reference', 'Unidad(es) de servicio', 0.01, 1.0, 1);

select setval('uom_uom_id_seq', (select max(id) from uom_uom));