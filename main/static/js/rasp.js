
$(document).ready(function() {
	
	var $window =  $(window);
	var $criteriaForm = $('#criteria-form');
	var top = $($criteriaForm).offset().top;

	/* В случае,если область просмотра шириной менее 580px, сделать меню сворачиваемым */
	var hiddenMenu = $('<button type="button" id="hiddenMenuBtn" class="btn btn-sm btn-block">Показать/скрыть критерии</button>');
	
	$window.ready(function() {
		if ($window.width() < 580) {
			$('#criteria-form').append(hiddenMenu);

			$("#hiddenMenuBtn").click(function() {
		  		if (!$('#criteria').is(':animated')) {
		  			$("#criteria").toggle('slow');
		  		}
			});
		}
		if ($window.width() >= 580) {
			$('#hiddenMenuBtn').remove();
			$('#criteria').show();
		}
	}); 

	
	/* форма прилипает к верху области просмотра */
	$window.scroll(function() {
		$criteriaForm.toggleClass('stick-top', 
			$window.scrollTop() > top);

		if ($window.scrollTop() > top) {
			$('#query-result').css('padding-top', $criteriaForm.height()+18 );
		}
		if ($window.scrollTop() <= top) {
			$('#query-result').css('padding-top', 0);
		}
	});

	$('.datepicker').datepicker({
			dateFormat:'dd.mm.yy',
		});

	/* Если в комментариях есть ОТМЕНА, строка становится красной */
	$('.comment-td').each(function() {
		var $this = $(this);
		if ($this.text().includes('ОТМЕНА')) {
			$this.parent().css('background-color', '#ff6666');
		}
		if ($this.text().includes('ИЗМЕНЕНИЕ')) {
			$this.parent().css('background-color', '#d7f442');
		}
	});
});

