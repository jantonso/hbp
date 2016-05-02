var selectedDate = '';
var errorMsg;
var minDate = null;
var maxDate = null;
var months = new Array();
months[0] = "January"; months[1] = "February"; months[2] = "March";
months[3] = "April"; months[4] = "May"; months[5] = "June";
months[6] = "July"; months[7] = "August"; months[8] = "September";
months[9] = "October"; months[10] = "November"; months[11] = "December";
var apptsHashMap = {};

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
		minDate: minDate,
		maxDate: maxDate,
		beforeShowDay: function(date) {
			var formattedDate = $.datepicker.formatDate('mm/dd/yy', date)
			if (formattedDate == selectedDate) {
				return [true, 'selectedDate'];
			} else {
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
					var appt_class;
					var a = appt_times[i];
					// If the appointment is booked, display it as so
					if (a.booked) {
						appt_class = 'appt-booked';
					} else {
						if (i % 2 == 0) {
							appt_class = 'appt-even';
						} else {
							appt_class = 'appt-odd';
						}
					}
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

		// Convert date to a standardized format
		a_date = moment(a_date, 'MM/DD/YYYY').format('MM/DD/YYYY');

		// Get the minimum and maximum dates, this assumes that
		// the appointments are sorted reverse chronologically
		if (i == 0) {
			minDate = a_date;
		} else if (i == appointments.length - 1) {
			maxDate = a_date;
		}
		var a_time = a.fields['appt_time'];
		var a_unit = a.fields['unit_name'];
		var a_booked = a.fields['booked'];
		if (apptsHashMap[a_date]) {
			apptsHashMap[a_date].push({'time': a_time, 'unit': a_unit, 
				'id': a.pk, 'booked': a_booked});
		} else {
			apptsHashMap[a_date] = [{'time': a_time, 'unit': a_unit, 
				'id': a.pk, 'booked': a_booked}];
		}
	}
	console.log(apptsHashMap);
}