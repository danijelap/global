$(function() {
	$( "#slider-range" ).slider({
		range: true,
		min: 0,
		max: 1000,
		values: [ 75, 300 ],
		slide: function( event, ui ) {
			$( "#cena" ).val( ui.values[ 0 ] + "-" + ui.values[ 1 ] );
		}
	});
	$( "#cena" ).val( $( "#slider-range" ).slider( "values", 0 ) +
		"-" + $( "#slider-range" ).slider( "values", 1 ) );
	ucitajSpisakStanova();
});

function vise(objekat_id) {
	$("#prazan").load("/nekretnine/detalji?id_stana=" + objekat_id);
}

function ucitajSpisakStanova() {
	filter_dictionary = {}
	grad = $("#grad").val()
	namestenost = $("#namestenost").val()
	tip_objekta = $("#tip_objekta").val()
	broj_soba = $("#broj_soba").val()
	if (grad != "0") filter_dictionary["grad"] = grad;
	if (namestenost != "0") filter_dictionary["namestenost"] = namestenost;
	if (tip_objekta != "0") filter_dictionary["tip_objekta"] = tip_objekta;
	if(broj_soba !="nista") filter_dictionary["broj_soba"] = broj_soba;
	$.get("/nekretnine/spisak", filter_dictionary, function(response){
		$("#spisak").html(response)
	});
}