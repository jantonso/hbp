$(document).ready(function() {
	$('.loading-message').hide();

	// Validation of form to make sure that all the fields are filled out
	$('form').validate({
		submitHandler: function(form) {
			$('.loading-message').show();
			return true;
		}
	});
});