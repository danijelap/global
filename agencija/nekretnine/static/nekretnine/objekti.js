$(function() {
	$( "#slider-range" ).slider({
		range: true,
		min: 0,
		max: 1000,
		values: [ 75, 300 ],
		slide: function( event, ui ) {
			$( "#amount" ).val( ui.values[ 0 ] + "-" + ui.values[ 1 ] );
		}
	});
	$( "#amount" ).val( $( "#slider-range" ).slider( "values", 0 ) +
		"-" + $( "#slider-range" ).slider( "values", 1 ) );
	$("select").chosen();
	$("#spisak").load("/nekretnine/spisak");
});

function vise(objekat_id) {
	$("#prazan").load("/nekretnine/detalji?id_stana=" + objekat_id);
}
