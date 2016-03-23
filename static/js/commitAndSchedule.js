var MIN_YEAR = 1900;
var CURRENT_YEAR = 2016;

// -------------------------------- 1: Commit -----------------------------------------

// Hide the commit  section, show the delivery date section
function onCommitClick() {
	$('#cs-commit').hide();
	$('#cs-delivery-date').show();
	$('#confirm-date-button').show();
}

// -------------------------------- 2: Delivery Date ----------------------------------

function checkDeliveryDate() {
	var day = document.getElementById('deliveryDay').value;
	var month = document.getElementById('deliveryMonth').value;
	var year = document.getElementById('deliveryYear').value;
	if (validateDate(day, month, year)) {
		// Store the delivery date in a new field
		var date = month + '/' + day + '/' + year;
		console.log('Date is valid!');
		$('#deliveryDate').value = date;

		// Hide the delivery date section, show the calendar section
		$('#cs-delivery-date').hide();
		$('#confirm-date-button').hide();
		$('#cs-calendar').show();
		$('#confirm-appt-button').show();
	} else {
		// Show error message
		console.log('Please enter a valid date...')
		$('#delivery-date-error-msg').text('That date is invalid. Please try again.');
		$('#delivery-date-error-msg').show();
	}
}

// -------------------------------- 3: Calendar ---------------------------------------

var selectedDate = '';

$(document).ready(function() {
	$('#calendar-container').datepicker({
		inline: true,
		firstDay: 1,
		showOtherMonths: true,
		dayNamesMin: ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'],
		dateFormat: 'MM-d-yy',
		beforeShowDay: function(date) {
			var formattedDate = $.datepicker.formatDate('MM-d-yy', date);
			if (formattedDate == selectedDate) {
				return [true, 'selectedDate'];
			} else {
				return [true, 'free'];
			}
		},
		onSelect: function(dateText, inst) {
			// Highlight the selected day
			selectedDate = dateText;

			var temp = dateText.split('-');
			var month = temp[0];
			var day = temp[1];
			var year = temp[2];

			// Display the appointments for that day
			$('#cs-calendar h2').hide();
			$('#cs-calendar #appt-container').show();
			$('#cs-calendar #appt-container #appt-month').text(month);
			$('#cs-calendar #appt-container #appt-day').text(day);	
		}
	});

	// When the user clicks on an appt, display it as selected
	$('#cs-calendar #appt-container .appt').click(function() {
		// Unselect old appt
		$('#cs-calendar #appt-container .appt p').css('color', '#7B8FB7');
		$('#cs-calendar #appt-container .appt-odd').css('background','#CDDEFF');
		$('#cs-calendar #appt-container .appt-even').css('background','#DCE7FD');		
		// Select this appt
		$(this).css('background', '#4E8DFF');
		$(this).children().css('color', '#FEFEFE');
	});
})

// Hide the calendar section, show the signature section
function getSignature() {
	$('#cs-calendar').hide();
	$('#confirm-appt-button').hide();
	$('#cs-signature').show();
	$('#confirm-sig-button').show();
}

// -------------------------------- 4: Signature --------------------------------------

function validateSigForm() {
	if (checkName() && checkDOBDate()) {
		return true
	} else {
		return false;
	}
}

// Make sure the name field is valid
function checkName() {
	var name = document.getElementById('sig-name').value;
	if (name != null && name != '') {
		return true;
	} else {
		console.log('Please enter your name.');
		$('#dob-error-msg').text('Please enter your name.');
		$('#dob-error-msg').show();
		return false;
	}
}

// Make sure the date of birth field is valid
function checkDOBDate() {
	var day = document.getElementById('dobDay').value;
	var month = document.getElementById('dobMonth').value;
	var year = document.getElementById('dobYear').value;
	if (validateDate(day, month, year)) {
		// Store value in a new dob field
		var date = month + '/' + day + '/' + year;
		$('#dobDate').value = date;
		return true;
	} else {
		// Display error message
		console.log('Please enter a valid date...')
		$('#dob-error-msg').text('That date is invalid. Please try again.');
		$('#dob-error-msg').show();
		return false;
	}
}

// -------------------------------- Helpers -------------------------------------------

// Check to make sure that the date is valid
function validateDate(day, month, year) {
	var isDay = /^[0-9]+$/.test(day);
	var isMonth = /^[0-9]+$/.test(month);
	var isYear = /^[0-9]+$/.test(year);

	// Check that the string contains only digits
	if (!isDay || !isMonth || !isYear) {
		return false;		
	}

	var dayValue = parseInt(day);
	var monthValue = parseInt(month);
	var yearValue = parseInt(year);

	// Check that the string can be converted to a number (should always be the case)
	if (isNaN(day)|| isNaN(month) || isNaN(year)) {
		return false;
	}

	// Check that the month is valid
	if (monthValue < 1 || monthValue > 12) {
		return false;
	}

	// Include leap year day by default... no extra checking for it
	// Since we only care about ~6 weeks out from delivery date it is okay
	var listOfDays = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
	// Check that the day is valid
	if (dayValue < 1 || dayValue > listOfDays[monthValue-1]) {
		return false;
	}

	// Check that the year is valid
	if (yearValue < MIN_YEAR || yearValue > CURRENT_YEAR) {
		return false;
	}

	return true;
}