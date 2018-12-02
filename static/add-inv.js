<!-- ///////////////////////// Add new investment ///////////////////////// -->
"use strict";

    function addNewInv(results) {
        // display investment by date
        console.log('hello');
        console.log(results);

    }

    function addInv(evt) {
        evt.preventDefault();
        let formInputs = {
            "company-name": $("#company-name").val(),
            "quantity": $("#quantity").val(),
            "cost": $("#cost").val(),
            "date": $("#inv-date").val(),
        };

        $.post("/add-investment.json", 
               formInputs,
               addNewInv);
    }

    $("#add-inv-form").on("submit", addInv);
