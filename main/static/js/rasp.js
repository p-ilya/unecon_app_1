
$(document).ready(function() {
	
	var $window =  $(window);
	var $criteriaForm = $('#criteria-form');
	var top = $($criteriaForm).offset().top;

	/* форма как боковой слайдер
	var sideMenu = $('<input type="button" id="sideMenuBtn" value="Критерии" class="btn"/>');
	
	$window.resize(function() {
		if ($window.width() < 550) {
			$('#criteria-form').prepend(sideMenu);
			$('#criteria').toggleClass('sidenav');
		}
		if ($window.width() >= 550) {
			$('#sideMenuBtn').remove();
		}
	}); 

	$('#sideMenuBtn').click(function() {
		$('#criteria').animate({'left': '0px'});
	});
	*/
	/* форма прилипает к верху области просмотра */
	$window.scroll(function() {
		$criteriaForm.toggleClass('stick-top', 
			$window.scrollTop() > top);

		if ($window.scrollTop() > top) {
			$('#query-result').css('padding-top', $criteriaForm.height() );
		}
		if ($window.scrollTop() <= top) {
			$('#query-result').css('padding-top', 0);
		}
	});

	$('.datepicker').datepicker({
			dateFormat:'dd.mm.yy',
		});

	$('.comment-td').each(function() {
		var $this = $(this);
		if ($this.text().includes('ОТМЕНА')) {
			$this.parent().css('background-color', '#ff6666');
		}
	});
});

