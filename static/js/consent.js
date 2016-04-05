var pCanvas;
var pSignaturePad;
var oCanvas;
var oSignaturePad;

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
});

function validateConsentForm() {
	if (checkParticipant() && checkObtainer()) {
		return true
	} else {
		return false;
	}
}

// Make sure the participant signed
function checkParticipant() {
	if (pSignaturePad.isEmpty()) {
		/* Display error message
		console.log('Please sign...');
		$('#sig-error-msg').text('Please provide a signature.');
		$('#sig-error-msg').show();*/
		return false;
	} else {
		// Add the base 64 string of the image to a hidden input field in form
		document.getElementById('id_participant_sig').value = pSignaturePad.toDataURL();
		return true;
	}
}

// Make sure the person obtaining consent signed
function checkObtainer() {
	if (oSignaturePad.isEmpty()) {
		/* Display error message
		console.log('Please sign...');
		$('#sig-error-msg').text('Please provide a signature.');
		$('#sig-error-msg').show();*/
		return false;
	} else {
		// Add the base 64 string of the image to a hidden input field in form
		document.getElementById('id_obtaining_sig').value = oSignaturePad.toDataURL();
		return true;
	}
}

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