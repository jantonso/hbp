var MIN_YEAR = 1900;
var CURRENT_YEAR = 2016;

function checkDate() {
	var day = document.getElementById('deliveryDay').value;
	var month = document.getElementById('deliveryMonth').value;
	var year = document.getElementById('deliveryYear').value;
	if (validateDate(day, month, year)) {
		var date = month + '/' + day + '/' + year;
		dateIsValid(date);
	} else {
		dateIsInvalid();
	}
}

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

function dateIsInvalid() {
	console.log('Please enter a valid date...')
	$('#error-msg').show();
}

function dateIsValid(date) {
	console.log('Date is valid!');
	$('#deliveryDate').value = date;

	// Hide the delivery date section, show the calendar section
	$('#cs-delivery-date').hide();
	$('#confirm-date-button').hide();
	$('#cs-calendar').show();
	$('#confirm-appt-button').show();
}

// Hide the commit message section, show the delivery date section
function onCommitClick() {
	$('#cs-commit').hide();
	$('#cs-delivery-date').show();
	$('#confirm-date-button').show();
}

// Hide the calendar section, show the signature section
function getSignature() {
	$('#cs-calendar').hide();
	$('#confirm-appt-button').hide();
	$('#cs-signature').show();
	$('#confirm-sig-button').show();
}
