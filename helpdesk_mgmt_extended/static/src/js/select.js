odoo.define('helpdesk.selection', function (require) {
    "use strict";

    var ajax = require("web.ajax");

    $(document).ready(function(){
        let select_one = document.getElementById("types");
        let select_two = document.getElementById("category");

        if(select_one) {
            document.getElementById("types").addEventListener("click", selection);

            function selection() {
                let selector = select_one.selectedIndex;
                switch (selector) {
                    case 1:
                        select_two.innerHTML = "";
                        ajax.jsonRpc('/nuevo/ticket', 'call', {team: 1}).then(function (data){
                            for(var i=0; i<data.length; i++) {
                                select_two.innerHTML += '<option value="'+data[i].id+'">'+data[i].name+'</option>';
                            }
                        });
                        break
                    case 2:
                        select_two.innerHTML = "";
                        ajax.jsonRpc('/nuevo/ticket', 'call', {team: 2}).then(function (data){
                            for(var i=0; i<data.length; i++) {
                                select_two.innerHTML += '<option value="'+data[i].id+'">'+data[i].name+'</option>';
                            }
                        });
                        break
                    case 3:
                        select_two.innerHTML = "";
                        ajax.jsonRpc('/nuevo/ticket', 'call', {team: 3}).then(function (data) {
                            for(var i=0; i<data.length; i++) {
                                select_two.innerHTML += '<option value="'+data[i].id+'">'+data[i].name+'</option>';
                            }
                        });
                        break
                }
            }
        }
    });
});
