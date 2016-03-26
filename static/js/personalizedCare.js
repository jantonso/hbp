// Check to make sure that all questions have been answered
function validatePCForm() {
	var allAnswered = true;
	$('input:radio').each(function() {
		var name = $(this).attr('name');
		if ($('input:radio[name='+name+']:checked').length == 0) {
			allAnswered = false;
		}
	})
	// If they didn't answer all the questions, display an error message
	if (!allAnswered) {
		$('.error-msg').show();
	}
	return allAnswered;
}