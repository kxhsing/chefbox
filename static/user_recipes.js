

       //Remove recipe from user's recipe box
      function deleteRecipe(evt) {
        evt.preventDefault();

        var thisButton = this;
        var thisDiv = thisButton.parentElement.parentElement.parentElement;


        var formInputs = {
          "recipe_id": this.value
        };


        $.post("/del_recipe", formInputs, function(){

          alert("Recipe removed.");
          $(thisDiv).fadeOut();


        });
      }

        $(".del-recipe").on('click', deleteRecipe);


      //Display instructions on click 
      $(".instructions-button").on("click", function(){
        var thisButton = this;
        var instructions = $(thisButton).siblings("ol.recipe-instructions");
        $(instructions).toggle();

        if ($(thisButton).text()=="View Instructions") {
        $(thisButton).text("Hide Instructions");
        }
        else {
          $(thisButton).text("View Instructions");
        }

        });

        //Mark recipe as cooked and move to Chef Board
      function reviewRecipe(evt) {
        evt.preventDefault();

        var thisButton = this;
        var thisDiv = thisButton.parentElement.parentElement.parentElement;


        var formInputs = {
          "recipe_id": this.value
        };


        $.post("/review_recipe", formInputs, function(){

          alert("Recipe moved to your Chef Board. Upload a photo & review the recipe there.");
          $(thisDiv).fadeOut();


        });
      }

        $(".review-recipe").on('click', reviewRecipe);




