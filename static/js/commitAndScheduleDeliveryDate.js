$(document).ready(function() {
	var errorMsg = $('#error-msg p');
	$('.loading-message').hide();

	// Auto tab date fields as the user types
	$('form #id_delivery_month').on('keypress', function(event) {
		// Make sure it is a numeric value or backspace, delete, tab, escape, enter
		if (event.charCode >= 48 && event.charCode <= 57) {
			if ($(this).val().length == 1) {
				$(this).next('input').focus();
			}
		} else if ($.inArray(event.keyCode, [46, 8, 9, 27, 13, 110, 190]) == -1) {
			event.preventDefault();
		}
	});

	// Auto tab date fields as the user types
	$('form #id_delivery_day').on('keypress', function(event) {
		// Make sure it is a numeric value or backspace, delete, tab, escape, enter
		if (event.charCode >= 48 && event.charCode <= 57) {
			if ($(this).val().length == 1) {
				$(this).next('input').focus();
			}
		} else if ($.inArray(event.keyCode, [46, 8, 9, 27, 13, 110, 190]) == -1) {
			event.preventDefault();
		}
	});

	$('form #id_delivery_year').on('keypress', function(event) {
		// Make sure it is a numeric value or backspace, delete, tab, escape, enter
		if (event.charCode >= 48 && event.charCode <= 57) {
			if ($(this).val().length == 4) {
				console.log("num");
			}
		} else if ($.inArray(event.keyCode, [46, 8, 9, 27, 13, 110, 190]) == -1) {
			event.preventDefault();
		}
	});

	// Validation of form to make sure that all the fields are filled out
	$('form').validate({
		rules: {
			q10: "required",
			q11: "required",
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
				errorMsg.text('Please enter a valid date.');
				errorMsg.show();
				return false;
			}

			$('.loading-message').show();
			return true;
		},
		// Display errors if a field is missing 
		showErrors: function(errorMap, errorList) {
			if (errorList.length > 0) {
				errorMsg.text('Please fill out the required fields.');
				errorMsg.show();
			}
		}
	});
});