/* Author: Lex Waldoch
    Date: 3/31/23
    Description: This JQuery script interacts with User.html to allow the user to temporariily upload profile information.
    Path: script.js*/

// When the document is ready, the following code will run.
$(document).ready(function () {
    var readURL = function (input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function (e) { // When the file is loaded, the profile picture will be changed to the uploaded image.
                $('.profile-pic').attr('src', e.target.result);
            }
            reader.readAsDataURL(input.files[0]); // (Temporary) Reads the file as a data URL, will have to be changed when the backend is functional.
        }
    }

    $(".file-upload").on('change', function () { // When the file is changed, the readURL function will run.
        readURL(this);
    });

    $(".upload-button").on('click', function () { // When the upload button is clicked, the file upload state will be 'clicked', which will trigger the change event.
        $(".file-upload").click();
    });
});

// Object to store the user's profile data
let userProfile = {
    fullName: '',
    email: ''
};

// Load the user's profile data into the input fields
$('#full-name').val(userProfile.fullName);
$('#email').val(userProfile.email);


// Save changes button click handler
$('#save-changes').click(function (event) {
    event.preventDefault(); // Prevent the default form submit behavior, we're not actually submitting a form

    const fullNameInput = $('#full-name');
    const emailInput = $('#email');

    // Update the user profile object with the new values
    userProfile.fullName = fullNameInput.val();
    userProfile.email = emailInput.val();

    // Disable all input fields
    fullNameInput.prop('disabled', true);
    emailInput.prop('disabled', true);
});
