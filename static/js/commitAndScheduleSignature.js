var MIN_YEAR = 1900;
var CURRENT_YEAR = 2016;
var canvas;
var signaturePad;

$(document).ready(function() {
	// Bring up the canvas to allow users to sign
	canvas = document.getElementById('signature-canvas');
	canvas.width = 800;
	canvas.height = 300;
	window.onresize = resizeCanvas;
	signaturePad = new SignaturePad(canvas);
});

function validateSigForm() {
	if (checkName() && checkDOBDate() && checkSignature()) {
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
		$('#sig-error-msg').text('Please enter your name.');
		$('#sig-error-msg').show();
		return false;
	}
}

// Make sure the date of birth field is valid
function checkDOBDate() {
	var day = document.getElementById('dobDay').value;
	var month = document.getElementById('dobMonth').value;
	var year = document.getElementById('dobYear').value;
	if (checkDate(day, month, year)) {
		return true;
	} else {
		// Display error message
		console.log('Please enter a valid date...')
		$('#sig-error-msg').text('That date is invalid. Please try again.');
		$('#sig-error-msg').show();
		return false;
	}
}

// Make sure the user signed
function checkSignature() {
	if (signaturePad.isEmpty()) {
		// Display error message
		console.log('Please sign...');
		$('#sig-error-msg').text('Please provide a signature.');
		$('#sig-error-msg').show();
		return false;
	} else {
		// save the image as png
		//signaturePad.toDataURL();
		return true;
	}
}

// Check to make sure that the date is valid
function checkDate(day, month, year) {
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

// Adjust canvas coordinate space taking into account pixel ratio,
// to make it look crisp on mobile devices.
function resizeCanvas() {
    var ratio =  Math.max(window.devicePixelRatio || 1, 1);
    canvas.width = canvas.offsetWidth * ratio;
    canvas.height = canvas.offsetHeight * ratio;
    canvas.getContext("2d").scale(ratio, ratio);
}