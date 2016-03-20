function validatePhoneNumber() {
	if (checkPhoneNumber()) {
		return true;
	} else {
		// Show error message
		console.log('invalid phone number.');
		$('#phone-number-error-msg').show();
		return false;
	}
}

function checkPhoneNumber() {
	var phoneNumber = document.getElementById('phone-number').value;
	console.log(phoneNumber);

	// Remove all non digit characters
	phoneNumber = phoneNumber.replace(/\D/g, '')
	console.log(phoneNumber);

	if (phoneNumber && phoneNumber.length == 10) {
		// Set the phone number field to the stripped phone number
		$('#phone-number').value = phoneNumber;
		return true;
	} else {
		return false;
	}
}