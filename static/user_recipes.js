

       //Remove recipe from user's recipe box
      function deleteRecipe(evt) {
        evt.preventDefault();

        var thisButton = this;
        var thisDiv = thisButton.parentElement.parentElement.parentElement;


        var formInputs = {
          "recipe_id": this.value
        };


        $.post("/del_recipe", formInputs, function(){

          // alert("Recipe removed.");
          $(thisButton).html("&#10004");
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
          // debugger;
          var cookedDiv = thisButton.parentElement.previousElementSibling;
          console.log(cookedDiv);
          $(thisButton).replaceWith("Recipe moved to Chef Board!");
          $(thisDiv).fadeOut(1000);


        });
      }

        $(".review-recipe").on('click', reviewRecipe);




