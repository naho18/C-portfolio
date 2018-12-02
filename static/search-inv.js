<!-- /////////////////// Search investment by date ///////////////////////// -->
"use strict";

    function displayInv(results) {
        // display investment by date
        console.log(results);
        var str = JSON.stringify(results, null, 2);
        $('#search-results').html(str);


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
