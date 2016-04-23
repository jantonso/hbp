var selectedDate = '';
var errorMsg;
var months = new Array();
months[0] = "January"; months[1] = "February"; months[2] = "March";
months[3] = "April"; months[4] = "May"; months[5] = "June";
months[6] = "July"; months[7] = "August"; months[8] = "September";
months[9] = "October"; months[10] = "November"; months[11] = "December";
var apptsHashMap = {}

$(document).ready(function() {

	// Process and convert appts to desired format
	processAppointments();

	errorMsg = $('#appt-container #appt-container-errors #error-msg p');

	$('#calendar-container').datepicker({
		inline: true,
		firstDay: 1,
		showOtherMonths: true,
		dayNamesMin: ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'],
		dateFormat: 'mm/dd/yy',
		beforeShowDay: function(date) {
			var formattedDate = $.datepicker.formatDate('mm/dd/yy', date);
			// Check to see if that day is selected
			if (formattedDate == selectedDate) {
				return [true, 'selectedDate'];
			} else {
				// Check to see if there is an appt on that day
				if (apptsHashMap[formattedDate]) {
					return [true, 'hasAppts'];
				} else {
					return [true, 'noAppts'];
				}
			}
		},
		onSelect: function(dateText, inst) {
			// Reset all selected appointments 
			resetAppointments();
			
			// Highlight the selected day
			selectedDate = dateText;

			// Show the appointment container
			$('#page-content #calendar-instructions').hide();
			$('#page-content #appt-container').show();

			// Show the appointment date on the container
			var d = new Date(dateText);
			var month = months[d.getMonth()];
			var day = d.getDate();
			$('#page-content #appt-container #appt-month').text(month);
			$('#page-content #appt-container #appt-day').text(day);	

			// Display the appointment times
			$('#page-content #appt-container #appt-container-times').empty();
			var appt_times = apptsHashMap[selectedDate];
			if (appt_times) {
				for (var i = 0; i <appt_times.length; i++) {
					var appt_class = 'appt-odd';
					if (i % 2 == 0) {
						appt_class = 'appt-even';
					}
					var a = appt_times[i];
					$('#page-content #appt-container #appt-container-times').append(
						$('<div/>', {'class': 'row'}).append(
							$('<div/>', {'class': 'col-lg-12 appt ' + appt_class, 'id': a['id']}).append(
								$('<p/>', {'class': 'appt-time', text: a['time']}),
								$('<p/>', {'class': 'appt-unit', text: a['unit']})
							).click(function() {
								// Unselect old appt
								resetAppointments();

								// Select this appt
								$(this).css('background', '#4E8DFF');
								$(this).children().css('color', '#FEFEFE');

								document.getElementById('id_appt_id').value = parseInt($(this).attr('id'));
							})
						)
					);
				}
			} else {
				$('#page-content #appt-container #appt-container-times').append(
					$('<div/>', {'class': 'row'}).append(
						$('<div/>', {'class': 'col-lg-12 appt appt-even'}).append(
							$('<p/>', {'class': 'appt-unit', text: 'There are no appointments on this day. Please select another day.'})
						)
					)
				);
			}
		}
	});

	// Validation of form to make sure that all the fields are filled out
	$('form').validate({
		ignore: [],
		rules: {
			appt_id: "required"
		},
		// Display errors if a field is missing 
		showErrors: function(errorMap, errorList) {
			if (errorList.length > 0) {
				errorMsg.show();
			}
		}
	});
});

// Resets any selected appointment
function resetAppointments() {
	document.getElementById('id_appt_id').value = null;
	$('#page-content #appt-container .appt p').css('color', '#7B8FB7');
	$('#page-content #appt-container .appt-odd').css('background','#CDDEFF');
	$('#page-content #appt-container .appt-even').css('background','#DCE7FD');	
	errorMsg.hide();
}

function processAppointments() {
	console.log(appointments);
	// Convert appointments into a hash map
	// Each date maps to an array of appt times
	for (var i = 0; i < appointments.length; i++) {
		var a = appointments[i];
		var a_date = a.fields['appt_date'];
		var a_time = a.fields['appt_time'];
		var a_unit = a.fields['unit_name'];
		if (apptsHashMap[a_date]) {
			apptsHashMap[a_date].push({'time': a_time, 'unit': a_unit, 'id': a.pk});
		} else {
			apptsHashMap[a_date] = [{'time': a_time, 'unit': a_unit, 'id': a.pk}];
		}
	}
	console.log(apptsHashMap);
}