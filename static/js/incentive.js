$(document).ready(function() {
	var errorMsg = $('#error-msg p');
	$('.loading-message').hide();

	// Make sure the phone number is valid
	$.validator.addMethod('validPhoneNumber', function(value, element) {
		// Remove all non digit characters
		var phoneNumber = value.replace(/\D/g, '')

		if (phoneNumber && phoneNumber.length == 10) {
			// Set the phone number field to the stripped phone number
			//$('#phone-number').value = phoneNumber;
			return true;
		} else {
			return false;
		}
	});

	// Validation of form to make sure that all the fields are filled out
	$('form').validate({
		rules: {
			phone_number: {
				required: true,
				validPhoneNumber: true
			}
		},
		submitHandler: function(form) {
			$('.loading-message').show();
			return true;
		},
		// Display errors if a field is missing 
		showErrors: function(errorMap, errorList) {
			if (errorList.length > 0) {
				errorMsg.show();
			}
		}
	});
});