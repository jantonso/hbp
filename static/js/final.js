$(document).ready(function() {
	$('.loading-message').hide();

	$('footer .print-button').click(function() {
		$('.loading-message').show();
	});
});