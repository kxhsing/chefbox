

       //Remove recipe from user's recipe box
       function deleteRecipe(evt) {
          evt.preventDefault();

          var thisButton = this;
          var thisTable = $(thisButton).parentsUntil("table");


          var formInputs = {
            "recipe_id": this.value
          };


          $.post("/del_recipe", formInputs, function(){

            alert("Recipe removed.");
            $(thisTable).fadeOut();


          });
        }

        $(".del-recipe").on('click', deleteRecipe);


        //Mark recipe as cooked and move to Chef Board
       function reviewRecipe(evt) {
          evt.preventDefault();

          var thisButton = this;
          var thisTable = $(thisButton).parentsUntil("table");


          var formInputs = {
            "recipe_id": this.value
          };


          $.post("/review_recipe", formInputs, function(){

            alert("Recipe moved to your Chef Board. Upload a photo & review the recipe there.");
            $(thisTable).fadeOut();


          });
        }

        $(".review-recipe").on('click', reviewRecipe);




