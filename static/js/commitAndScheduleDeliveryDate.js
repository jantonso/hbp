$(document).ready(function() {
	// Validation of form to make sure that all the fields are filled out
	$('form').validate({
		rules: {
			delivery_month: "required",
			delivery_day: "required",
			delivery_year: "required"
		},
		// Before submitting makes sure the date is valid
		submitHandler: function(form) {
			var dDay = form.elements['delivery_day'].value;
			var dMonth = form.elements['delivery_month'].value;
			var dYear = form.elements['delivery_year'].value;
			if (!checkDate(dDay, dMonth, dYear)) {
				$('#delivery_date-error-msg').show();
				return false;
			}
			return true;
		},
		// Display errors if a field is missing 
		showErrors: function(errorMap, errorList) {
			$('#delivery-date-error-msg').show();
		}
	});
}

function validateDeliveryDate() {
	var day = document.getElementById('id_delivery_day').value;
	var month = document.getElementById('id_delivery_month').value;
	var year = document.getElementById('id_delivery_year').value;
	if (checkDate(day, month, year)) {
		return true;
	} else {
		// Show error message
		$('#delivery-date-error-msg').text('That date is invalid. Please try again.');
		$('#delivery-date-error-msg').show();
		return false;
	}
}