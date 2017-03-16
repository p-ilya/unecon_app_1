
$(document).ready(function() {

	var $window =  $(window);
	var $criteriaForm = $('#criteria-form');
	var top = $($criteriaForm).offset().top;

	$window.scroll(function() {
		$criteriaForm.toggleClass('stick-top', 
			$window.scrollTop() > top);
	});

});