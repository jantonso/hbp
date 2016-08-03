$(document).ready(function() {
	$('.loading-message').hide();

	$('footer .next-button').click(function() {
		$('.loading-message').show();
	});
});