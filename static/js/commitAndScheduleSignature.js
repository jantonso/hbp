var canvas;
var signaturePad;

$(document).ready(function() {
	var errorMsg = $('#error-msg p');

	// Bring up the canvas to allow users to sign
	canvas = document.getElementById('signature-canvas');
	canvas.width = 800;
	canvas.height = 220;
	signaturePad = new SignaturePad(canvas);

	window.onresize = resizeCanvas;

	// Check to make sure the user signed
	$.validator.addMethod('signatureNotEmpty', function(value, element) {
		if (signaturePad.isEmpty()) {
			return false;
		} else {
			document.getElementById('id_sig_image').value = signaturePad.toDataURL();
			return true;
		}
	});

	// Validation of form to make sure that all the fields are filled out
	$('form').validate({
		ignore: [],
		rules: {
			// Make sure each field is non empty, including the signatures
			sig_image: {
				signatureNotEmpty: true
			},
			sig_name: "required",
			dob_month: "required",
			dob_day: "required",
			dob_year: "required"
		},
		messages: {
			sig_image: "Please provide a signature.",
			sig_name: "Please enter your name.",
			dob_month: "Please enter a valid date.",
			dob_day: "Please enter a valid date.",
			dob_year: "Please enter a valid date.",
		},
		// Before submitting makes sure the dates are valid
		submitHandler: function(form) {

			// Validate the dob date
			var dobDay = form.elements['dob_day'].value;
			var dobMonth = form.elements['dob_month'].value;
			var dobYear = form.elements['dob_year'].value;
			if (!checkDate(dobDay, dobMonth, dobYear)) {
				errorMsg.text('Please enter a valid date.');
				errorMsg.show();
				return false;
			}

			return true;
		},
		// Display errors if a field is missing 
		showErrors: function(errorMap, errorList) {
			if (errorList.length > 0) {
				errorMsg.text(errorList[0].message);
				errorMsg.show();
			}
		}
	});
});

// Adjust Canvas coordinate space taking into account pixel ratio,
// to make it look crisp on mobile devices.
function resizeCanvas() {
    var ratio =  Math.max(window.devicePixelRatio || 1, 1);
    
    canvas.width = canvas.offsetWidth * ratio;
    canvas.height = canvas.offsetHeight * ratio;
    canvas.getContext("2d").scale(ratio, ratio);
}