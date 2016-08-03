var pCanvas;
var oCanvas;

$(document).ready(function() {
	$('.loading-message').hide();
	var pErrorMsg = $('form #participant-error-msg p');
	var oErrorMsg = $('form #obtaining-error-msg p');

	// Bring up the pCanvas to allow participant to sign
	pCanvas = document.getElementById('participant-signature');
	pCanvas.width = 920;
	pCanvas.height = 150;
	var pSignaturePad = new SignaturePad(pCanvas);

	// Bring up the oCanvas to allow person obtaining consent to sign
	oCanvas = document.getElementById('obtaining-signature');
	oCanvas.width = 920;
	oCanvas.height = 150;
	var oSignaturePad = new SignaturePad(oCanvas);

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
		messages: {
			participant_sig: "Please provide a signature for the participant.",
			participant_name: "Please enter a name for the participant.",
			participant_month: "Please enter a date for the participant.",
			participant_day: "Please enter a date for the participant.",
			participant_year: "Please enter a date for the participant.",
			obtaining_sig: "Please provide a signature for the person obtaining consent.",
			obtaining_name: "Please enter a name for the person obtaining consent.",
			obtaining_role: "Please enter the role for the person obtaining consent.",
			obtaining_month: "Please enter a date for the person obtaining consent.",
			obtaining_day: "Please enter a date for the person obtaining consent.",
			obtaining_year: "Please enter a date for the person obtaining consent."
		},
		// Before submitting makes sure the dates are valid
		submitHandler: function(form) {

			// Validate the participant's date
			var pDay = form.elements['participant_day'].value;
			var pMonth = form.elements['participant_month'].value;
			var pYear = form.elements['participant_year'].value;
			if (!checkDate(pDay, pMonth, pYear)) {
				oErrorMsg.hide();
				pErrorMsg.text('Please enter a valid date for the participant.');
				pErrorMsg.show();
				return false;
			}

			// Validate the obtainer's date
			var oDay = form.elements['obtaining_day'].value;
			var oMonth = form.elements['obtaining_month'].value;
			var oYear = form.elements['obtaining_year'].value;
			if (!checkDate(oDay, oMonth, oYear)) {
				pErrorMsg.hide();
				oErrorMsg.text('Please enter a valid date for the person obtaining consent.');
				oErrorMsg.show();
				return false;
			}

			$('.loading-message').show();
			return true;
		},
		// Display errors if a field is missing 
		showErrors: function(errorMap, errorList) {
			if (errorList.length > 0) {
				var errorMsg = errorList[0].message;
				var errorMsgSplit = errorMsg.split(" ");
				// Figure out if it is a participant error for the person obtaining consent
				if (errorMsgSplit[errorMsgSplit.length-1] == 'participant.') {
					oErrorMsg.hide();
					pErrorMsg.text(errorList[0].message);
					pErrorMsg.show();
				} else {
					pErrorMsg.hide();
					oErrorMsg.text(errorList[0].message);
					oErrorMsg.show();
				}
			}
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