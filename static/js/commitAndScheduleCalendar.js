var selectedDate = '';
var selectedAppt = '';
var errorMsg;
var months = new Array();
months[0] = "January"; months[1] = "February"; months[2] = "March";
months[3] = "April"; months[4] = "May"; months[5] = "June";
months[6] = "July"; months[7] = "August"; months[8] = "September";
months[9] = "October"; months[10] = "November"; months[11] = "December";


$(document).ready(function() {
	console.log(appointments);

	errorMsg = $('#appt-container #error-msg p');

	$('#calendar-container').datepicker({
		inline: true,
		firstDay: 1,
		showOtherMonths: true,
		dayNamesMin: ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'],
		dateFormat: 'mm/dd/yy',
		beforeShowDay: function(date) {
			var formattedDate = $.datepicker.formatDate('mm/dd/yy', date);
			if (formattedDate == selectedDate) {
				return [true, 'selectedDate'];
			} else {
				// Figure out if this date has any appointments or not
				for (var i = 0; i < appointments.length; i++) {
					if (appointments[i].fields['appt_date'] == formattedDate) {
						console.log("We got an appt on: " + formattedDate);
						return [true, 'hasAppts'];
					}
				}
				return [true, 'noAppts'];
			}
		},
		onSelect: function(dateText, inst) {
			// Highlight the selected day
			selectedDate = dateText;

			var d = new Date(dateText);

			var month = months[d.getMonth()];
			var day = d.getDate();

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