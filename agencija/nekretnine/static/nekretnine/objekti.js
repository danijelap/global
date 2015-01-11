$(function() {
	window.kliknuto_na_dugme = false;
	$("#filter_range_slider").slider({
		range: true,
		slide: function( event, ui ) {
			$(window.active_filter_range + "_value").val( ui.values[ 0 ] + "-" + ui.values[ 1 ] );
		}
	});
	
	ucitajSpisakStanova();
	$(document).click(function(){
		if (!window.kliknuto_na_dugme) {
				$("#novi_filteri").hide();
				$("#filter_range_slider").hide();
		}
		window.kliknuto_na_dugme = false;
	});
	
	window.svi_filteri = ['grad', 'namestenost', 'tip_objekta', 'cena']
	window.prikazani_filteri = []
	dodajFilter('grad');
	dodajFilter('namestenost');
});

function init_filter_slider(slider_id) {
	jq_filter_slider_id = "#" + slider_id;
	$(jq_filter_slider_id).mouseover(function(){
		var filter_position = $(jq_filter_slider_id).offset();
		var new_slider_position = filter_position;
		new_slider_position.top += 25;
		$("#filter_range_slider").slider( "option", "max", $(jq_filter_slider_id + "_max").val());
		$("#filter_range_slider").slider( "option", "min", $(jq_filter_slider_id + "_min").val());
		$("#filter_range_slider").slider( "option", "values", $(jq_filter_slider_id + "_value").val().split('-'));
		$("#filter_range_slider").show().css(new_slider_position);
		window.active_filter_range = jq_filter_slider_id;
	});
}

function vise(objekat_id) {
	$("#prazan").load("/nekretnine/detalji?id_stana=" + objekat_id);
}

function ucitajSpisakStanova() {
	var filter_dictionary = {};
	filters = $("#filteri").find("[id^=filter_]").filter("[id$=_value]");
	filters.each(function(index, element) {
		filter_id = element.id.substring(7, element.id.length-6);
		filter_value = $(element).val();
		if (filter_value != "0") {
			console.log(filter_id + "=" + filter_value);
			filter_dictionary[filter_id] = filter_value;
		}
	})
	$.get("/nekretnine/spisak", filter_dictionary, function (response) {
		$("#spisak").html(response);
	});
}
function sakrijFilter(id_filtera) {
	$("#filter_" + id_filtera).remove();
	index_of_filter = window.prikazani_filteri.indexOf(id_filtera);
	if (index_of_filter > -1) {
		window.prikazani_filteri.splice(index_of_filter, 1);
	}
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