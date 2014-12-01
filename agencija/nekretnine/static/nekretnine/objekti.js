$(function() {
	$( "#slider-range" ).slider({
		range: true,
		min: 0,
		max: 800,
		values: [ 75, 300 ],
		slide: function( event, ui ) {
			$( "#amount" ).val( ui.values[ 0 ] + "-" + ui.values[ 1 ] );
		}
	});
	$( "#amount" ).val( $( "#slider-range" ).slider( "values", 0 ) +
		"-" + $( "#slider-range" ).slider( "values", 1 ) );
});

$(function vise() {
	$("#prazan").load("/nekretnine/detalji?id_stana ={{ objekat.id }}");
});