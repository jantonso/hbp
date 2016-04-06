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
	var participantName = document.getElementById('id_participant_name').value;
	if (checkName(participantName, 'Please enter a name for the participant.') 
		&& checkSignature(pSignaturePad, 'id_participant_sig', 
			'Please provide a signature for the participant.')) {
		return true;
	} else {
		return false;
	}
}

// Make sure the person obtaining consent signed
function checkObtainer() {
	var obtainingName = document.getElementById('id_obtaining_name').value;
	if (checkName(obtainingName, 'Please enter a name for the person obtaining consent.') 
		&& checkSignature(oSignaturePad, 'id_obtaining_sig', 
			'Please provide a signature for the person obtaining consent.')) {
		return true;
	} else {
		return false;
	}
}

// --------------------------------------------- Helpers --------------------------------------- 

// Make sure the name field is valid
function checkName(name, errorMsg) {
	if (name != null && name != '') {
		return true;
	} else {
		console.log('Please enter your name.');
		$('#error-msg').text(errorMsg);
		$('#error-msg').show();
		return false;
	}
}

// Make sure the user signed
function checkSignature(signaturePad, sigFieldID, errorMsg) {
	if (signaturePad.isEmpty()) {
		// Display error message
		console.log('Please sign...');
		$('#error-msg').text(errorMsg);
		$('#error-msg').show();
		return false;
	} else {
		// Add the base 64 string of the image to a hidden input field in form
		document.getElementById(sigFieldID).value = signaturePad.toDataURL();
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