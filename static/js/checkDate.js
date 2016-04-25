var dayFormats = ['D', 'DD'];
var monthFormats = ['M', 'MM', 'MMM', 'MMMM'];
var yearFormats = ['YYYY', 'YY'];

// Check to make sure that the date is valid
function checkDate(day, month, year) {

	var date = month + '/' + day + '/' + year;
	for (var i = 0; i < dayFormats.length; i++) {
		for (var j = 0; j < monthFormats.length; j++) {
			for (var k = 0; k < yearFormats.length; k++) {
				var dFmt = dayFormats[i];
				var mFmt = monthFormats[j];
				var yFmt = yearFormats[k];
				if (moment(date, mFmt + '/' + dFmt + '/' + yFmt).isValid()) {
					return true;
				}
			}
		}
	}

	return false;
}