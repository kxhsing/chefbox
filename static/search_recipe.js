

    //if user has ingredients in inventory but want to add more before submitting recipe search query
      function ingredAddResult(result) {
        console.log(result);
        var ingredList = $("#ingred-list");
        var ingredientName = result.ingredient;
        if (ingredientName) {
        var ingredID = result.ingred_id;
        console.log(ingredID);
        ingredList[0].innerHTML = ingredList.html() + '<li><input type="checkbox" name="search_ingredients" value="'+ingredientName+'" checked>'+ingredientName+'</li>';
        alert("Added to inventory and search query: "+ingredientName);
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


    //if no ingredients in inventory and want to add ingredients to search
      function newIngredAddResult(result) {
      console.log(result);
      var ingredList = $("#new-ingred-list");
      var ingredientName = result.ingredient;
      if (ingredientName) {
      var ingredID = result.ingred_id;
      console.log(ingredID);
      ingredList[0].innerHTML = ingredList.html() + '<li><input type="checkbox" name="search_ingredients" value="'+ingredientName+'" checked>'+ingredientName+'</li>';
      alert("Added to inventory and search query: "+ingredientName);
      }
      else {
        alert("Ingredient exists already");
        };
    }

    function addNewIngred(evt) {
      evt.preventDefault();

      var formInputs = {
        "ingredient": $("#new-ingredient").val()
      };

      $.post("/add_ingred", formInputs, newIngredAddResult);
    }

    $("#new-ingred").on("submit", addNewIngred);




