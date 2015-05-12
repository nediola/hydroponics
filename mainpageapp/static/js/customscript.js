$(function() {
	$('.openeditform').bind('click', function() {
		onclick_gardenbed($(this).attr('gardenbed-id'));
	});

});

/* Shows edit-form for current gardenbed */
function onclick_gardenbed(gb_id) {
	$.ajax({    
	    type: 'GET',                                                                                                                                                                                            
	  	url: '/get_gardenbed/',
	  	data: { gardenbed_id: gb_id},                                                                                                                                              
	    dataType: 'jsonp', 
	    jsonpCallback: "fill_edit_form",
	    error: function(xhr, text_status, exception ) {alert('Baaaaad')}                                                                                                                                                                                           
   	});
}


function fill_edit_form(jsonp)
{
	//results_amount = jsonp.amount;
	//$('#results_number').text("Результатов: " + results_amount);	

	var modal_title = $('#modal-title');
	//modal_title.append(gardenbed_id);
	var modal_sel_plant_name = $("#sel-plant-name");
	var modal_sel_plant_mix = $("#sel-plant-mix");
}

function mouse_over() {
	//Show info
	//document.getElementById("button").src="../images/button2.png";
}
	
function mouse_out() {
	//Stop show info
	//document.getElementById("button").src="../images/button1.png";
}