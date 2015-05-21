$(function() {
});

function checkform() {
	var ingredient_ids = []
	$('.select-tank-ingredient').each(function() {
		if ($(this).val() != 0) {
			ingredient_ids.push($(this).val())
		}
	});
	var unique_ingredient_ids = [];
	$.each(ingredient_ids, function(i, el){
    	if($.inArray(el, unique_ingredient_ids) === -1) unique_ingredient_ids.push(el);
	});
	if (ingredient_ids.length != unique_ingredient_ids.length){
		alert('В нескольких резервуарах не может быть один и тот же ингредиент')
		return false;
	}
	return true;
}