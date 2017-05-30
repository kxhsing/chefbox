
      // Add ingredient to inventory; stays on current page
      function ingredAddResult(result) {
        console.log(result);
        var ingredList = $("#ingred-list");
        var ingredientName = result.ingredient;
        if (ingredientName) {
        var ingredID = result.ingred_id;
        console.log(ingredID);
        ingredList[0].innerHTML = ingredList.html() + '<tr><td>'+ingredientName+'</td><td><form action="/del_ingred" method="post"><button type="submit" class="delete-button btn btn-outline-secondary btn-sm" name="ingredient" value="'+ingredID+'">&times;</button></form></td></tr>';

        // alert("Added to inventory: " + ingredientName);
        // $(".delete-button").on('click', delIngred);
        var alertDiv = document.createElement("div"); 
        $(alertDiv).addClass("alert alert-success alert-dismissible");
        $(alertDiv).attr("role", "alert");
        $(alertDiv).append('<button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>Added to inventory: <strong>'+ ingredientName+'</strong>');
        $(alertDiv).appendTo("#alert-area");

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
        evt.preventDefault();
        var formInputs = {
          "ingredient": this.value
        };

        var thisButton = this;
        var thisIngred = this.parentElement.parentElement.previousElementSibling;
        var thisTR = this.parentElement.parentElement.parentElement;

        $.post("/del_ingred", formInputs, function(){
          $(thisTR).remove();

          alert("Removed from inventory: "+ thisIngred.innerText);


        });;
      }

      $("#ingred-list").on('click', ".delete-button", delIngred);


      


