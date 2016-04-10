$(document).ready(function() {
	var errorMsg = $('#questions-container #error-msg p');

	// Validation of form to make sure that all the fields are filled out
	$('form').validate({
		rules: {
			q1: "required",
			q2: "required",
			q3: "required",
			q4: "required",
			q5: "required",
			q6: "required",
			q7: "required",
			q8: "required",
			q9: "required"
		},
		// Display errors if a field is missing 
		showErrors: function(errorMap, errorList) {
			errorMsg.show();
		}
	});
});