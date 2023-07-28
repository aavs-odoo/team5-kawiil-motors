odoo.define('ge10_team05.motorcycles', ['web.ajax'], function(require) {
    'use strict';
    const ajax = require('web.ajax');
    $(document).ready(function () {
        let container = document.getElementById("products");
        if(container){
            container.innerHTML="";
            container.innerHTML="<div class='col text-center'>Cargando Kilometraje</div>"
            ajax.jsonRpc("/get_products", 'call', {}).then(function(data){
                container.innerHTML="";
                console.log("Hola");
                console.log(data);
                for(let i=0; i<data.length; i++){
                    container.innerHTML += '<div class="col-12 col-sm-6 col-md-4 col-lg-4 mb-3">\
                                                <h6 class="text-center mt-3 pb-1">Registry Number: '+data[i].name+'</h6>\
                                                <h6 class="text-center mt-3 pb-1">Mileage = '+data[i].mileage+'</h6>\
                                                <h6 class="text-center mt-3 pb-1">Vin = '+data[i].vin+'</h6>\
                                            </div>';
                }
            })
        }

    })
});
