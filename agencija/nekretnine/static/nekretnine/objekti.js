$(function() {
	window.kliknuto_na_dugme = false;
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
	$(document).click(function(){
		if (!window.kliknuto_na_dugme) {
				$("#novi_filteri").hide();
		}
		window.kliknuto_na_dugme = false;
	});
});

function vise(objekat_id) {
	$("#prazan").load("/nekretnine/detalji?id_stana=" + objekat_id);
}

function ucitajSpisakStanova() {
	var filter_dictionary = {};
	var grad = $("#grad").val();
	var namestenost = $("#namestenost").val();
	var tip_objekta = $("#tip_objekta").val();
	var broj_soba = $("#broj_soba").val();
	if (grad != "0") filter_dictionary["grad"] = grad;
	if (namestenost != "0") filter_dictionary["namestenost"] = namestenost;
	if (tip_objekta != "0") filter_dictionary["tip_objekta"] = tip_objekta;
	if(broj_soba !="nista") filter_dictionary["broj_soba"] = broj_soba;
	$.get("/nekretnine/spisak", filter_dictionary, function (response) {
		$("#spisak").html(response);
	});
}
function sakrijFilter(id_filtera) {
	$(id_filtera).hide();
}

function prikaziIzborNovogFiltera() {
	window.kliknuto_na_dugme = true;
	var pozicija_dugmeta = $("#dugme_dodaj_filter").offset();
	var pozicija_izbora = pozicija_dugmeta;
	pozicija_izbora.left += 30;
	pozicija_izbora.top += 25;
	$("#novi_filteri").show()
		.css(pozicija_izbora)
		.load('/nekretnine/filteri');
}

function dodajFilter(ime_filtera) {
	// pozvati $get kao u funkciji ucitajSpisakStanova, u filter_dictionary ubaciti promenljivu ime_filtera, a u view-u koji budes napravila treba da se napravi trazeni filter
	// u funkciji koja obradjuje odgovor od view-a pozvati append umesto html (html brise sve i stavlja ovo sto si joj dala, a append dodaje)
}