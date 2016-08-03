$(document).ready(function() {
	$('.loading-message').hide();

	$('footer .next-button').click(function() {
		$('#video-links .video-link').hide();
		$('#videos-container iframe').hide();
		$('.loading-message').show();
	});

	$('footer .back-button').click(function() {
		$('#videos-container iframe').hide();
		$('.loading-message').show();
	});
});