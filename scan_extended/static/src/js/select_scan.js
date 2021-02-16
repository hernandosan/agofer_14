odoo.define('scan_extended.agofer', function (require) {
    "use strict";

    let account_invoice = [
        "IEA",
        "IED",
        "IEE",
        "IEK",
        "IEL",
        "IEM",
        "IEN",
        "IEO",
        "IEP",
        "IEQ",
        "IER",
        "IES",
        "IET",
        "IEV",
        "IEW",
        "IEX",
        "IEY",
        "IEZ",
        "CFA",
        "CFC",
        "CFK",
        "CFL",
        "CFM",
        "CFN",
        "CFO",
        "CFP",
        "CFQ",
        "CFR",
        "CFS",
        "CFT",
        "CFV",
        "CFW",
        "CFX",
        "CFY",
        "CFZ"
    ];
    let sucs = [
        "ARM",
        "BAR",
        "BOG",
        "BUC",
        "BUG",
        "CAL",
        "CAR",
        "IBA",
        "ITA",
        "MAL",
        "NEI",
        "PAL",
        "PAS",
        "PER",
        "VIL",
        "RIC",
        "MAR",
        "MON"
    ];
    let stock_picking_sub2 = [
        "01",
        "04",
        "05",
        "14",
        "19"
    ];
    let stock_picking_sub3 = [
        "OUT",
        "INT",
        "IN"
    ];

    function populate_options(id, arr) {
        $(arr).each(function (i) {
            $(id).append($('<option/>').val(arr[i]).text(arr[i]));
        });
    }

    $(document).ready(function () {
        let select_one = document.getElementById("type_document");
        let select_two = document.getElementById("prefix_document");
        let current_year = new Date().getFullYear();

        if (select_one) {
            document.getElementById("type_document").addEventListener("change", selection);

            function selection() {
                let selector = select_one.value;
                $("#prefix_document").show();
                $("#prefix_document").empty();
                $("#prefix2_document").empty();
                $("#prefix2_document").attr('style', 'display:none');
                $("#prefix3_document").empty();
                $("#prefix3_document").attr('style', 'display:none');

                switch (selector) {
                    case "account.move":
                        select_two.innerHTML = "";
                        $("#prefix_document").append("<option>--Selection--</option>");
                        populate_options('#prefix_document', account_invoice);
                        break;
                    case "sale.order":
                        select_two.innerHTML = "";
                        $("#prefix_document").append(`<option>PV/${current_year}/</option>`);
                        break;
                    case "stock.picking":
                        select_two.innerHTML = "";
                        $("#prefix_document").append("<option>--Selection--</option>");
                        populate_options('#prefix_document', sucs);
                        $("#prefix2_document").attr('style', 'display:block');
                        populate_options('#prefix2_document', stock_picking_sub2);
                        $("#prefix3_document").attr('style', 'display:block');
                        populate_options('#prefix3_document', stock_picking_sub3);
                        break;
                    case "delivery.guide":
                        select_two.innerHTML = "";
                        $("#prefix_document").append(`<option>GUIA</option>`);
                        break;
                    case "account.payment":
                        select_two.innerHTML = "";
                        $("#prefix_document").append(`<option>EGF/${current_year}</option>`);
                        $("#prefix2_document").append("<option>--Selection--</option>").attr('style', 'display:block');
                        populate_options('#prefix2_document', sucs);
                        break;
                    case "mrp.production":
                        select_two.innerHTML = "";
                        $("#prefix_document").append(`<option>MO</option>`);
                        $("#prefix_document").append(`<option>PO</option>`);
                        $('<input/>').attr('name', 'prefix2').attr('id', 'prefix2')
                            .attr('type', 'hidden')
                            .val('/').insertAfter($("#prefix_document"));
                        break;
                    default:
                        select_two.innerHTML = "";
                        $("#prefix_document").append("<option>--Selection--</option>");
                        break;
                }
            }

            $("#add-files-button").click(function () {
                let last_file = $('form input:file').last();
                let count_file = ($('form input:file').length) + 1;
                $("<input/>", {
                    "class": "form-control o_website_form_input",
                    "type": "file",
                    "name": "attachment",
                    "id": "attachment",
                    "multiple": "multiple"
                }).insertAfter(last_file);
            });
        }
    });
});

