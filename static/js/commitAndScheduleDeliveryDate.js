var MIN_YEAR = 1900;
var CURRENT_YEAR = 2016;

function validateDeliveryDate() {
	var day = document.getElementById('deliveryDay').value;
	var month = document.getElementById('deliveryMonth').value;
	var year = document.getElementById('deliveryYear').value;
	if (checkDate(day, month, year)) {
		return true;
	} else {
		// Show error message
		$('#delivery-date-error-msg').text('That date is invalid. Please try again.');
		$('#delivery-date-error-msg').show();
		return false;
	}
}