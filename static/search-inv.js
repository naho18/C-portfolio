<!-- /////////////////// Search investment by date ///////////////////////// -->
"use strict";

    function displayInv(results) {
        // display investment by date
        var str = JSON.stringify(results, null, '  ');
        $('#search-results').html("<pre>" + "<code>" + str + "</pre>" + "</code>");


    }

    function searchInv(evt) {
        evt.preventDefault();
        let formInputs = {
            "date": $("#date").val(),
        };

        $.get("/investments-by-date.json", 
               formInputs,
               displayInv);
    }

    $("#search-inv-form").on("submit", searchInv);
