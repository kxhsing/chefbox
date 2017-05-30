    $(document).ready(function() {
      var win = $(window);

      // Each time the user scrolls
      win.scroll(function() {
        // End of the document reached?
        if ($(document).height() - win.height() == win.scrollTop()) {
          // $(".load-on-bottom").show();

          $.ajax({
            type: 'POST',
            url: "/search_more",
            data: {"more_results": 10},
            success: function(data) {

              if (parseInt(data.total_results) > 10){
                $(".load-on-bottom").show();
                
              }
              else {
                $(".load-on-bottom").hide();
              }

              console.log(data);

              for (i = 0; i < data.recipe_results_list.length; i++) {
                var newDiv = document.createElement("div"); 
                $(newDiv).addClass("card");

                var newTitleBlock = document.createElement("div"); 
                $(newTitleBlock).addClass("card-block");
                var recipeTitle = data.recipe_results_list[i][1];

                if ((data.recipe_results_list[i][2]) && (data.recipe_results_list[i][3])){
                  var sourceName = data.recipe_results_list[i][2];
                  var sourceUrl = data.recipe_results_list[i][3];
                  $(newTitleBlock).append('<h4 class="card-title">'+recipeTitle+'</h4><p class="card-text">via <a href="'+sourceUrl+'" target="_blank" class="card-link">'+sourceName+'</a></p>');
                }
                else if (data.recipe_results_list[i][3]){
                  var sourceName = "[Original Source]";
                  var sourceUrl = data.recipe_results_list[i][3];
                  $(newTitleBlock).append('<h4 class="card-title">'+recipeTitle+'</h4><p class="card-text">via <a href="'+sourceUrl+'" target="_blank" class="card-link">'+sourceName+'</a></p>');
                }
                else {
                  var sourceName = data.recipe_results_list[i][2];
                  $(newTitleBlock).append('<h4 class="card-title">'+recipeTitle+'</h4><p class="card-text">via'+sourceName+'</a></p>');
                }
                $(newTitleBlock).appendTo(newDiv);

                var newImage = document.createElement("img"); 
                var imgUrl = data.recipe_results_list[i][4];
                $(newImage).addClass("card-img-top img-fluid");
                $(newImage).attr("src", imgUrl);
                $(newImage).appendTo(newDiv);

                var newBlock = document.createElement("div"); 
                $(newBlock).addClass("card-block");
                var ingredList = document.createElement("ul");

                for (y = 0; y < data.recipe_results_list[i][6].length; y++) {
                  var li = document.createElement("li");
                  li.appendChild(document.createTextNode(String(data.recipe_results_list[i][6][y])));
                  ingredList.appendChild(li);
                }


                var instructList = document.createElement("ol");
                $(instructList).addClass("recipe-instructions");
                for (z = 0; z < data.recipe_results_list[i][5].length; z++) {
                  var li = document.createElement("li");
                  li.appendChild(document.createTextNode(data.recipe_results_list[i][5][z]));
                  instructList.appendChild(li);

                }

                var recipeID = data.recipe_results_list[i][0];

                $(newBlock).append('<h5>Ingredients</h5>');
                $(newBlock).append(ingredList);
                $(newBlock).append('<button type="button" class="instructions-button btn btn-outline-info">View Instructions</button><br>');
                $(newBlock).append(instructList);
                $(newBlock).append('<form action="/add_recipe" method="POST"><button type="submit" class="add-recipe btn btn-primary" name="recipe_id" value="'+recipeID+'">Save Recipe</button></form>');
                $(newBlock).appendTo(newDiv);

                $(newDiv).appendTo(".card-columns");

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


                $(".add-recipe").on('click', addRecipe);
                
              }
          }
          });
        }
      });
    });


     function addRecipe(evt) {
      evt.preventDefault();
      var thisButton = this;
      var thisDiv = thisButton.parentElement.parentElement.parentElement;


      var formInputs = {
        "recipe_id": this.value
      };


      $.post("/add_recipe", formInputs, function(){

        alert("Recipe saved!");
        $(thisDiv).fadeOut();


      });
      }

      $(".add-recipe").on('click', addRecipe);

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

