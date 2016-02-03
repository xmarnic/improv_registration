$(document).ready(function() {

	// Adds active class if form element has value
	$('input').on({
		'blur': function() {
			if ($(this).val() !== '') {
				$(this).addClass('active');
			} else {
				$(this).removeClass('active');
			}
		}
	});
	
});
