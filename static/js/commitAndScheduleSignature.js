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

// Adjust canvas coordinate space taking into account pixel ratio,
// to make it look crisp on mobile devices.
function resizeCanvas() {
    var ratio =  Math.max(window.devicePixelRatio || 1, 1);
    canvas.width = canvas.offsetWidth * ratio;
    canvas.height = canvas.offsetHeight * ratio;
    canvas.getContext("2d").scale(ratio, ratio);
}