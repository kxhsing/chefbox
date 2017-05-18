
      // Add ingredient to inventory; stays on current page
      function ingredAddResult(result) {
        console.log(result);
        var ingredList = $("#ingred_list");
        var ingredientName = result.ingredient;
        if (ingredientName) {
        var ingredID = result.ingred_id;
        console.log(ingredID);
        ingredList[0].innerHTML = ingredList.html() + '<li>'+ingredientName+'</li> <form action="/del_ingred" method="post"> <button type="submit" class="delete-button" name="ingredient" class="delete-button" value="'+ingredID+'">x</button></form>';
        alert("Added to inventory: " + ingredientName);
        // $(".delete-button").on('click', delIngred);
        }
        else {
          alert("Ingredient exists already");
        };
      }

      function addIngred(evt) {
        evt.preventDefault();

        var formInputs = {
          "ingredient": $("#ingredient").val()
        };

        $.post("/add_ingred", formInputs, ingredAddResult);

      }

      $("#add-ingred").on("submit", addIngred);


      // Delete ingredient from inventory; stays on current page
      function delIngred(evt) {
        console.log('in delIngred');
        evt.preventDefault();


        var formInputs = {
          "ingredient": this.value
        };

        var thisButton = this;
        var thisForm = $(thisButton).parent();
        var thisButtonIngred = thisForm.prev();


        $.post("/del_ingred", formInputs, function(){
          thisButton.remove();
          thisButtonIngred.remove();

          alert("Removed from inventory: "+ $(thisButtonIngred).text());

        });
      }

      $("#ingred_list").on('click', ".delete-button", delIngred);


      


