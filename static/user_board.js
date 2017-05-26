//Remove recipe from UserRecipe
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

//Display upload photo form on click 
$(".upload-button").on("click", function(){
  var thisButton = this;
  var uploadForm = $(thisButton).siblings("form.upload-form");
  $(uploadForm).toggle();
  // if ($(thisButton).text()=="Upload Photo" || $(thisButton).text()=="Update Photo") {
  // $(thisButton).text("Cancel");
  // }
  // else {
  //   $(thisButton).text("Upload Photo");
  // }   

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
  $.ajax({
      type: 'POST',
      url: this.action,
      data: form_data,
      contentType: false,
      cache: false,
      processData: false,
      async: false,
      success: function(data) {
        if (data) {
          alert("Photo uploaded!");
          $(uploadButton).text("Update Photo");        
          var newPhoto = $(thisForm).siblings("div.photo-with-credit");
          newPhoto.html('<img src="/static/photos/'+data.photo+'"><br>Photo by '+data.firstname+' '+data.lastname);
        }
        else {
          alert("Not a valid photo file. Please try again."); //why is this not working?
        }

      }
  });

}

$(".upload-form").on("submit", uploadPhoto);



function deletePhoto(evt) {
  evt.preventDefault();
  var thisButton = this;
  // debugger;
  var thisForm = this.parentElement;
  var recipeID = this.value;
  var thisDiv = $(thisForm).siblings("div.photo-with-credit");
  var uploadButton = $(thisForm).siblings("button.upload-button");

  var formInputs = {
    "recipe_id": recipeID
  };

  $.post("/del_photo", formInputs, function(){

    alert("Photo deleted.");
    thisDiv.empty();
    thisButton.remove();
    uploadButton.text("Upload Photo");

  });
}

$(".delete-photo-btn").on('click', deletePhoto);



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
    alert("Recipe reviewed!");
    var newReview = result.review;
    thisDiv.text(newReview);
    thisDiv.show();

  });
}

$(".review-form").on("submit", writeReview);

