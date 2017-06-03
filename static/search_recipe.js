

    //if user has ingredients in inventory but want to add more before submitting recipe search query
      function ingredAddResult(result) {
        console.log(result);
        var ingredList = $("#ingred-list");
        var ingredientName = result.ingredient;
        if (ingredientName) {
          var ingredID = result.ingred_id;
          console.log(ingredID);
          ingredList[0].innerHTML = ingredList.html() + '<li class="search-checkbox"><input type="checkbox" name="search_ingredients" value="'+ingredientName+'" checked> '+ingredientName.charAt(0).toUpperCase()+ingredientName.slice(1)+'</li>';
          var alertDiv = document.createElement("div"); 
          $(alertDiv).addClass("alert alert-success alert-dismissible");
          $(alertDiv).attr("role", "alert");
          $(alertDiv).append('<button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>Added to inventory and search query: <strong>'+ ingredientName.charAt(0).toUpperCase()+ingredientName.slice(1)+'</strong>');
          $(alertDiv).appendTo("#search-alerts");
        }
        else {
          var alertDiv = document.createElement("div"); 
          $(alertDiv).addClass("alert alert-warning alert-dismissible");
          $(alertDiv).attr("role", "alert");
          $(alertDiv).append('<button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>Ingredient exists already.');
          $(alertDiv).appendTo("#search-alerts");
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
        ingredList[0].innerHTML = ingredList.html() + '<li class="search-checkbox"><input type="checkbox" name="search_ingredients" value="'+ingredientName+'" checked> '+ingredientName.charAt(0).toUpperCase()+ingredientName.slice(1)+'</li>';
        // alert("Added to inventory and search query: "+ingredientName);
        var alertDiv = document.createElement("div"); 
        $(alertDiv).addClass("alert alert-success alert-dismissible");
        $(alertDiv).attr("role", "alert");
        $(alertDiv).append('<button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>Added to inventory and search query: <strong>'+ ingredientName.charAt(0).toUpperCase()+ingredientName.slice(1)+'</strong>');
        $(alertDiv).appendTo("#search-alerts");
      }
      else {
          var alertDiv = document.createElement("div"); 
          $(alertDiv).addClass("alert alert-warning alert-dismissible");
          $(alertDiv).attr("role", "alert");
          $(alertDiv).append('<button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>Ingredient exists already.');
          $(alertDiv).appendTo("#search-alerts");
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




