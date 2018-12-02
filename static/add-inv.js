<!-- ///////////////////////// Add new investment ///////////////////////// -->
"use strict";

    function addNewInv(results) {
        console.log(results);        
        window.location.reload();
    }

    function addInv(evt) {
        evt.preventDefault();

        let formInputs = {
            "company-name": $("#company-name").val(),
            "quantity": $("#quantity").val(),
            "cost": $("#cost").val(),
            "date": $("#inv-date").val(),
        };

        $.get("/add-investment.json", 
               formInputs,
               addNewInv);
    }

    $("#add-inv-form").on("submit", addInv);
