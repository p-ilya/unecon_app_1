
$(document).ready(function() {
	
	$('.comment-td').each(function() {
		var $this = $(this);
		if ($this.text().includes('ОТМЕНА')) {
			$this.parent().css('background-color', '#ff6666');
		}
	});
});

