$(function() {
	$('#btnWish').click(function (){

		$.ajax({
			url: '/writeWish',
			data: $('form').serialize(),
			type: 'POST',
			success: function(response){
				console.log(response);
			},
			error: function(error){
				console.log(error);
			}
		});
	});
});
