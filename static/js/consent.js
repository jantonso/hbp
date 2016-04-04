var pCanvas;
var pSignaturePad;

$(document).ready(function() {
	// Bring up the pCanvas to allow users to sign
	pCanvas = document.getElementById('participant-signature');
	pCanvas.width = 920;
	pCanvas.height = 150;
	window.onresize = resizeCanvas;
	pSignaturePad = new SignaturePad(pCanvas);
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

// Adjust pCanvas coordinate space taking into account pixel ratio,
// to make it look crisp on mobile devices.
function resizeCanvas() {
    var ratio =  Math.max(window.devicePixelRatio || 1, 1);
    pCanvas.width = pCanvas.offsetWidth * ratio;
    pCanvas.height = pCanvas.offsetHeight * ratio;
    pCanvas.getContext("2d").scale(ratio, ratio);
}