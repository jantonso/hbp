var selectedDate = '';
var selectedAppt = '';

$(document).ready(function() {
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
			$('#cs-calendar h2').hide();
			$('#cs-calendar #appt-container').show();
			$('#cs-calendar #appt-container #appt-month').text(month);
			$('#cs-calendar #appt-container #appt-day').text(day);	

			// Reset all selected appointments 
			resetAppointments();
		}
	});

	// When the user clicks on an appt, display it as selected
	$('#cs-calendar #appt-container .appt').click(function() {
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
	$('#cs-calendar #appt-container .appt p').css('color', '#7B8FB7');
	$('#cs-calendar #appt-container .appt-odd').css('background','#CDDEFF');
	$('#cs-calendar #appt-container .appt-even').css('background','#DCE7FD');	
}

// Confirms that the user selected an appointment
function confirmAppt() {
	if (selectedAppt != '') {
		return true;
	} else {
		$('#cs-calendar #appt-container .error-msg').show();
		return false;
	}
}