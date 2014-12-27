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
	
	window.svi_filteri = ['Gradovi', 'Namestenost', 'Tip objekta']
	window.prikazani_filteri = ['Gradovi', 'Namestenost']
	for (i in window.prikazani_filteri) {
		dodajFilter(window.prikazani_filteri[i])
	}
});

function vise(objekat_id) {
	$("#prazan").load("/nekretnine/detalji?id_stana=" + objekat_id);
}

function ucitajSpisakStanova() {
	var filter_dictionary = {};
	var grad = $("#select_grad").val();
	var namestenost = $("#select_namestenost").val();
	var tip_objekta = $("#select_tip_objekta").val();
	if (grad != "0") filter_dictionary["grad"] = grad;
	if (namestenost != "0") filter_dictionary["namestenost"] = namestenost;
	if (tip_objekta != "0") filter_dictionary["tip_objekta"] = tip_objekta;
	$.get("/nekretnine/spisak", filter_dictionary, function (response) {
		$("#spisak").html(response);
	});
}
function sakrijFilter(id_filtera) {
	$(id_filtera).remove();
}

function prikaziIzborNovogFiltera() {
	window.kliknuto_na_dugme = true;
	var pozicija_dugmeta = $("#dugme_dodaj_filter").offset();
	var pozicija_izbora = pozicija_dugmeta;
	pozicija_izbora.left += 30;
	pozicija_izbora.top += 25;
	
	var novi_filteri = $(window.svi_filteri).not(window.prikazani_filteri).get();
	var filter_dictionary = {'filteri': novi_filteri};
	$.get('/nekretnine/filteri', filter_dictionary, function(response){
		$("#novi_filteri").show()
			.css(pozicija_izbora)
			.html(response);
	});
	
}

function dodajFilter(ime_filtera) {
	// pozvati $get kao u funkciji ucitajSpisakStanova, u filter_dictionary ubaciti promenljivu ime_filtera, a u view-u koji budes napravila treba da se napravi trazeni filter
	// u funkciji koja obradjuje odgovor od view-a pozvati append umesto html (html brise sve i stavlja ovo sto si joj dala, a append dodaje)
	var filter_dictionary = {'ime_filtera': ime_filtera};
	$.get("/nekretnine/napravi_filter", filter_dictionary, function (response) {
		window.prikazani_filteri.push(ime_filtera);
		$("#filteri").append(response);
	});
}