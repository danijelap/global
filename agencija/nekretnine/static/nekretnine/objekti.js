$(function() {
	$.cookie.json = true;
	init_slider_for_filters();
	init_document_click();
	
	detalji_css = $(window).height() - $("#filteri").height();
	spisak_css = $(window).height() - $("#filteri").height() - $("#favoriti").height();
	
	
	
	window.svi_filteri = ['grad', 'namestenost', 'tip_objekta', 'cena', 'broj_soba'];
	window.prikazani_filteri = [];
	start_filters = $.cookie('filters');
	if (typeof start_filters === 'undefined') {
		start_filters = ['grad', 'namestenost'];
	}
	
	dodajFiltere(start_filters);
	ucitajSpisakStanova();
	
	$("#spisak").css(spisak_css);
	$("#detalji").css(detalji_css);
});

function add_favorits(id_objekta) {
	if ($("#stan_" + id_objekta).parents("#spisak").lenght == 1) {
		x = $("#stan_" + id_objekta).remove();
		$("#favoriti").append(x);
	} else {
		x = $("#stan_" + id_objekta).remove();
		$("#spisak").append(x);
	}
}

function init_slider_for_filters() {
	$("#filter_range_slider").slider({
		range: true,
		slide: function(event, ui) {
			$(window.active_filter_range + "_value").val( ui.values[ 0 ] + "-" + ui.values[ 1 ] );
		},
		stop: function(event, ui) {
			ucitajSpisakStanova();
		}
	});
}

function init_document_click(){
	window.new_filters_button_clicked = false;
	$(document).click(function(){
		if (!window.new_filters_button_clicked) {
			$("#novi_filteri").hide();
			$("#filter_range_slider").hide();
		}
		window.new_filters_button_clicked = false;
	});
}

function init_filter_slider(slider_id) {
	jq_filter_slider_id = "#" + slider_id;
	$(jq_filter_slider_id).mouseover(function(event){
		filter_id = '#' + this.id;
		var filter_position = $(filter_id).offset();
		var new_slider_position = filter_position;
		new_slider_position.top += 25;
		$("#filter_range_slider").slider( "option", "max", $(filter_id + "_max").val());
		$("#filter_range_slider").slider( "option", "min", $(filter_id + "_min").val());
		$("#filter_range_slider").slider( "option", "values", $(filter_id + "_value").val().split('-'));
		$("#filter_range_slider").show().css(new_slider_position);
		window.active_filter_range = filter_id;
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
		$.cookie('filters', window.prikazani_filteri, {expires: 30});
	}
}

function prikaziIzborNovogFiltera() {
	window.new_filters_button_clicked = true;
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

function dodajFiltere(niz_filtera) {
	// pozvati $get kao u funkciji ucitajSpisakStanova, u filter_dictionary ubaciti promenljivu ime_filtera, a u view-u koji budes napravila treba da se napravi trazeni filter
	// u funkciji koja obradjuje odgovor od view-a pozvati append umesto html (html brise sve i stavlja ovo sto si joj dala, a append dodaje)
	var filter_dictionary = {'niz_filtera': niz_filtera};
	$.get("/nekretnine/napravi_filtere", filter_dictionary, function (response) {
		for (filter in niz_filtera) {
			window.prikazani_filteri.push(niz_filtera[filter]);
		}
		$("#filteri").append(response);
		$.cookie('filters', window.prikazani_filteri, {expires: 30});
	});
}