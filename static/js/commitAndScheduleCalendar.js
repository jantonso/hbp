var selectedDate = '';
var selectedAppt = '';
var errorMsg;

$(document).ready(function() {
	errorMsg = $('#appt-container #error-msg p');

	$('#calendar-container').datepicker({
		inline: true,
		firstDay: 1,
		showOtherMonths: true,
		dayNamesMin: ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'],
		dateFormat: 'MM-d-yy',
		beforeShowDay: function(date) {
			var formattedDate = $.datepicker.formatDate('MM-d-yy', date);
			if (formattedDate == selectedDate) {
				return [true, 'selectedDate'];
			} else {
				return [true, 'free'];
			}
		},
		onSelect: function(dateText, inst) {
			// Highlight the selected day
			selectedDate = dateText;

			var temp = dateText.split('-');
			var month = temp[0];
			var day = temp[1];
			var year = temp[2];

			// Display the appointments for that day
			$('#page-content #calendar-instructions').hide();
			$('#page-content #appt-container').show();
			$('#page-content #appt-container #appt-month').text(month);
			$('#page-content #appt-container #appt-day').text(day);	

			// Reset all selected appointments 
			resetAppointments();
		}
	});

	// When the user clicks on an appt, display it as selected
	$('#page-content #appt-container .appt').click(function() {
		// Unselect old appt
		resetAppointments();

		// Select this appt
		selectedAppt = $(this).find('.appt-time').text();
		$(this).css('background', '#4E8DFF');
		$(this).children().css('color', '#FEFEFE');
	});
})

// Resets any selected appointment
function resetAppointments() {
	selectedAppt = '';
	$('#page-content #appt-container .appt p').css('color', '#7B8FB7');
	$('#page-content #appt-container .appt-odd').css('background','#CDDEFF');
	$('#page-content #appt-container .appt-even').css('background','#DCE7FD');	
}

// Confirms that the user selected an appointment
function confirmAppt() {
	if (selectedAppt != '') {
		return true;
	} else {
		errorMsg.show();
		return false;
	}
}