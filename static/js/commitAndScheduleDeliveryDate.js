var MIN_YEAR = 1900;
var CURRENT_YEAR = 2016;

function validateDeliveryDate() {
	var day = document.getElementById('id_delivery_day').value;
	var month = document.getElementById('id_delivery_month').value;
	var year = document.getElementById('id_delivery_year').value;
	if (checkDate(day, month, year)) {
		return true;
	} else {
		// Show error message
		$('#delivery-date-error-msg').text('That date is invalid. Please try again.');
		$('#delivery-date-error-msg').show();
		return false;
	}
}