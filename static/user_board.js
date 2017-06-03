//Remove recipe from UserRecipe
// function deleteRecipe(evt) {
//   evt.preventDefault();

//   var thisButton = this;
//   var thisTable = $(thisButton).parentsUntil("table");


//   var formInputs = {
//     "recipe_id": this.value
//   };

//   $.post("/del_recipe", formInputs, function(){

//     alert("Recipe removed.");
//     $(thisTable).fadeOut();

//   });
// }

// $(".del-recipe").on('click', deleteRecipe);


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


$(".card-columns").on('click', ".delete-photo-btn", function (evt) {
  evt.preventDefault();
  var thisButton = this;

  var thisForm = this.parentElement;
  var recipeID = this.value;
  var thisDiv = $(thisForm).siblings("div.photo-with-credit");
  debugger;
  var uploadButton = $(thisForm).siblings("button.upload-button");

  var formInputs = {
    "recipe_id": recipeID
  };

  $.post("/del_photo", formInputs, function(){

    // alert("Photo deleted.");
    thisDiv.empty();
    thisButton.remove();
    uploadButton.text("Upload Photo");

  });
});



//Display upload photo form on click 
$(".upload-button").on("click", function(){
  var thisButton = this;
  // debugger;
  var uploadForm = $(thisButton).siblings("form.upload-form");
  $(uploadForm).toggle(); 

  });


//AJAX post request to upload/update photo
function uploadPhoto(evt) {
  evt.preventDefault();

  var thisForm = this;
  var thisAction = this.action;
  var thisPhotoInput = this.firstElementChild;
  var recipeID = thisPhotoInput.nextElementSibling.nextElementSibling.value;
  var uploadButton = $(this).siblings("button.upload-button");


  var form_data = new FormData(thisForm);
  if (form_data.get('photo').name && (form_data.get('photo').type=="image/jpeg" || form_data.get('photo').type=="image/png")) {
  
  $.ajax({
      type: 'POST',
      url: this.action,
      data: form_data,
      contentType: false,
      cache: false,
      processData: false,
      async: false,
      success: function(data) {
          // alert("Photo uploaded!");
          $(uploadButton).text("Update Photo");        
          var newPhoto = $(thisForm).siblings("div.photo-with-credit");
          newPhoto.html('<img class="card-img-top img-fluid" src="/static/photos/'+data.photo+'"><br>Photo by '+data.firstname+' '+data.lastname);
          var newDelButton = $(thisForm).siblings("div.new-del-button");
          newDelButton.html('<form action="/del_photo" method="POST" class="del-photo"><button type="submit" class="delete-photo-btn btn btn-secondary btn-sm" name="review_id" value="'+recipeID+'">Delete Photo</button><input type="hidden" name="recipe_id" value="'+recipeID+'"></form>');
          
          $(".delete-photo-btn").on('click', function(){

            evt.preventDefault();
            var thisButton = this;
            var thisForm = this.parentElement;
            var recipeID = this.value;
            var thisDiv = $(thisForm).siblings("div.photo-with-credit");
            var formInputs = {
              "recipe_id": recipeID
            };

            $.post("/del_photo", formInputs, function(){
              // alert("Photo deleted.");
              thisDiv.empty();
              thisButton.remove();
            });

            newPhoto.empty();
            newDelButton.empty();

          });
      }
  });
}

else {
  // alert("Not a valid photo file!");
  var alertDiv = document.createElement("div"); 
  $(alertDiv).addClass("alert alert-warning alert-dismissible");
  $(alertDiv).attr("role", "alert");
  $(alertDiv).append('<button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>Not a valid photo file!');
  $(alertDiv).appendTo("#alert-area");
}
}

$(".upload-form").on("submit", uploadPhoto);



//Display editable review form on click
function displayEditForm(){
  var thisButton = this;
  var thisForm = $(thisButton).siblings("form"); 
  var thisDiv = $(thisButton).siblings("div.review");
  $(thisForm).toggle();
  $(thisDiv).toggle();
  if (thisButton.innerText=="Edit Review" || thisButton.innerText=="Review Recipe") {
    thisButton.innerText = "Cancel";
  }
  else {
    thisButton.innerText = "Edit Review";
  }
}
$(".edit-review-btn").on("click", displayEditForm);



//AJAX post request to write new review/edit existing review
function writeReview(evt) {
  evt.preventDefault();
  var thisForm = this;
  var thisDiv = $(this).siblings("div.review");
  var reviewTextarea = this.firstElementChild;
  var recipeID = $(reviewTextarea).next().next().val();
  var review = reviewTextarea.value;

  var formInputs = {
    "recipe_id": recipeID,
    "review": review
  };

  var button = $(thisForm).siblings("button.edit-review-btn");
  if (review==""){
    button.text("Review Recipe");
  }
  else {
    button.text("Edit Review");
  }

  $.post("/write_review", formInputs, function (result) {
    console.log(result);
    $(thisForm).hide();
    // alert("Recipe reviewed!");
    var newReview = result.review;
    thisDiv.text(newReview);
    thisDiv.show();

  });
}

$(".review-form").on("submit", writeReview);
