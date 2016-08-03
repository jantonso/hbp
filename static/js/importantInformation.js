$(document).ready(function() {
	$('.loading-message').hide();

	$('footer .next-button').click(function() {
		$('.loading-message').show();
	});

	$('footer .back-button').click(function() {
		$('.loading-message').css('float', 'left');
		$('.loading-message').show();
	});

	$('#video-links .video-link').click(function() {
		console.log("sup");
		$('.loading-message').css('float', 'none');
		$('.loading-message').css('margin-left', 'auto');
		$('.loading-message').css('margin-right', 'auto');
		$('.loading-message').show();
	});
});