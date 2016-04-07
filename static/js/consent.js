var pCanvas;
var pSignaturePad;
var oCanvas;
var oSignaturePad;

/*var nameErrorMsg = 'Please enter a name for the participant.';
var dateErrorMsg = 'Please provide a valid date for the participant.';
var sigErrorMsg = 'Please provide a signature for the participant.'; */

$(document).ready(function() {

	// Bring up the pCanvas to allow participant to sign
	pCanvas = document.getElementById('participant-signature');
	pCanvas.width = 920;
	pCanvas.height = 150;
	pSignaturePad = new SignaturePad(pCanvas);

	// Bring up the oCanvas to allow person obtaining consent to sign
	oCanvas = document.getElementById('obtaining-signature');
	oCanvas.width = 920;
	oCanvas.height = 150;
	oSignaturePad = new SignaturePad(oCanvas);

	window.onresize = resizeCanvas;

	// Check to make sure the participant signed
	$.validator.addMethod('pSignatureNotEmpty', function(value, element) {
		if (pSignaturePad.isEmpty()) {
			return false;
		} else {
			document.getElementById('id_participant_sig').value = pSignaturePad.toDataURL();
			return true;
		}
	});

	// Check to make sure the person obtaining consent signed
	$.validator.addMethod('oSignatureNotEmpty', function(value, element) {
		if (oSignaturePad.isEmpty()) {
			return false;
		} else {
			document.getElementById('id_obtaining_sig').value = oSignaturePad.toDataURL();
			return true;
		}
	});

	// Validation of form to make sure that all the fields are filled out
	$('form').validate({
		ignore: [],
		rules: {
			// Make sure each field is non empty, including the signatures
			participant_sig: {
				pSignatureNotEmpty: true
			},
			participant_name: "required",
			participant_month: "required",
			participant_day: "required",
			participant_year: "required",
			obtaining_sig: {
				oSignatureNotEmpty: true
			},
			obtaining_name: "required",
			obtaining_role: "required",
			obtaining_month: "required",
			obtaining_day: "required",
			obtaining_year: "required"
		},
		// Before submitting makes sure the dates are valid
		submitHandler: function(form) {

			// Validate the participant's date
			var pDay = form.elements['participant_day'].value;
			var pMonth = form.elements['participant_month'].value;
			var pYear = form.elements['participant_year'].value;
			if (!checkDate(pDay, pMonth, pYear)) {
				$('#error-msg').text('Please enter a validate date for the participant.');
				$('#error-msg').show();
				return false;
			}

			// Validate the obtainer's date
			var oDay = form.elements['obtaining_day'].value;
			var oMonth = form.elements['obtaining_month'].value;
			var oYear = form.elements['obtaining_year'].value;
			if (!checkDate(oDay, oMonth, oYear)) {
				$('#error-msg').text('Please enter a validate date for the person obtaining consent.');
				$('#error-msg').show();
				return false;
			}

			return true;
		},
		// Display errors if a field is missing 
		showErrors: function(errorMap, errorList) {
			console.log(errorMap);
			console.log(errorList);
			$('#error-msg').text('There were errors...');
			$('#error-msg').show();
		}
	});
});

// Adjust Canvas coordinate space taking into account pixel ratio,
// to make it look crisp on mobile devices.
function resizeCanvas() {
    var ratio =  Math.max(window.devicePixelRatio || 1, 1);
    
    pCanvas.width = pCanvas.offsetWidth * ratio;
    pCanvas.height = pCanvas.offsetHeight * ratio;
    pCanvas.getContext("2d").scale(ratio, ratio);

    oCanvas.width = oCanvas.offsetWidth * ratio;
    oCanvas.height = oCanvas.offsetHeight * ratio;
    oCanvas.getContext("2d").scale(ratio, ratio);
}