window.sliderOptions=
{
	sliderId: "image_slider_big",
	startSlide: 0,
	effect: "13,17,13,13,5",
	effectRandom: true,
	pauseTime: 2600,
	transitionTime: 500,
	slices: 12,
	boxes: 9,
	hoverPause: 1,
	autoAdvance: true,
	captionOpacity: 1,
	captionEffect: "fade",
	thumbnailsWrapperId: "image_slider_small",
	m: false,
	license: "b6t80"
};
window.isImageSliderLoaded = false;

window.libFilter = {
	loadAvailableFilters: function(onComplete) {
		$.get("/nekretnine/get_filter_list/", function (response) {
			window.libFilter.availableFilters = response;
			window.libFilter.shownFilters = {};
			onComplete();
		}, 'json');
	},
	showFilters: function() {
		startFilters = $.cookie('filters');
		if (typeof startFilters === 'undefined') {
			startFilters = {};
			for (filter_id in this.availableFilters) {
				if (this.availableFilters[filter_id]['default']) {
					startFilters[filter_id] = 0;
				}
			}
		}
		this.appendFilters(startFilters);
	},
	appendFilters: function(filterDictionary) {
		var filterArray = [];
		for (filter_id in filterDictionary) {
			filterArray.push(filter_id);
		}
		$.get("/nekretnine/make_filters", {'filter_array': filterArray}, function (response) {
			$("#filters").append(response);
			for (filter_id in filterDictionary) {
				window.libFilter.shownFilters[filter_id] = filterDictionary[filter_id];
				$("#filter_" + filter_id + "_value").val(filterDictionary[filter_id]).change(function(event){
					element = event.target;
					filter_id = element.id.substring(7, element.id.length - 6);
					window.libFilter.shownFilters[filter_id] = $(element).val();
					$.cookie('filters', window.libFilter.shownFilters, {expires: 30});
				}).trigger("chosen:updated");
				if (window.libFilter.availableFilters[filter_id]['depends_on']) {
					dependsOnFilterId = window.libFilter.availableFilters[filter_id]['depends_on'];
					$("#filter_" + dependsOnFilterId + "_value").change(function(event) {
						dependsOnFilterElement = event.target;
						dependsOnFilterId = dependsOnFilterElement.id.substring(7, dependsOnFilterElement.id.length - 6);
						dependentFilterId = window.libFilter.getDependentFilter(dependsOnFilterId);
						dependsOnFilterValue = $(dependsOnFilterElement).val();
						window.libFilter.loadDependentFilter(dependentFilterId, dependsOnFilterValue);
					});
				}
				
				if (window.libFilter.availableFilters[filter_id]['depends_on']) {
					dependsOnFilterId = window.libFilter.availableFilters[filter_id]['depends_on'];
					dependsOnFilterValue = $("#filter_" + dependsOnFilterId + "_value").val()
					window.libFilter.loadDependentFilter(filter_id, dependsOnFilterValue);
				}
			}
			$.cookie('filters', window.libFilter.shownFilters, {expires: 30});
		});
	},
	getDependentFilter: function(dependsOnFilterId) {
		for (filter_id in this.availableFilters) {
			if (this.availableFilters[filter_id]['depends_on'] == dependsOnFilterId) {
				return filter_id;
			}
		}
		return null;
	},
	loadDependentFilter: function(dependentFilterId, dependsOnFilterValue) {
		filterDictionary = {
			'dependent_filter_id': dependentFilterId,
			'depends_on_filter_value': dependsOnFilterValue
		};
		$.get("/nekretnine/get_filter_content", filterDictionary, function (response) {
			$("#filter_" + dependentFilterId + "_value").empty();
			$("#filter_" + dependentFilterId + "_value").html(response);
			$("#filter_" + dependentFilterId + "_value").val(window.libFilter.shownFilters[dependentFilterId])
			$("#filter_" + dependentFilterId + "_value").trigger('chosen:updated').change();
		});
	}

};

$(function() {
	$.cookie.json = true;
	init_slider_for_filters();
	init_document_click();
	
	setHeightOfContainers();
	$(window).resize(setHeightOfContainers);
	
	window.libFilter.loadAvailableFilters(function() {
		window.libFilter.showFilters();
		ucitajSpisakStanova();
	});
	
	
});

function add_favorits(id_objekta) {
	if ($("#stan_" + id_objekta).parents("#spisak").length == 1) {
		x = $("#stan_" + id_objekta).remove();
		$("#favoriti").append(x);
	} else {
		x = $("#stan_" + id_objekta).remove();
		$("#spisak").append(x);
	}
	favoriti = $("#favoriti").find("[id^=stan_]");
	favorites_total_height = 0;
	favoriti.each(function(index, element){
		favorites_total_height += $(element).height();
	});
	maximum_height = 200
	if (favorites_total_height <= maximum_height) {
		$("#favoriti").css('height', favorites_total_height);
	} else {
		$("#favoriti").css('height', maximum_height);
	}
	setHeightOfContainers();
}

function setHeightOfContainers() {
	// prvi nacin podesavanja css-a pomocu jQuery-ja. $(element).css(osobina, vrednost);
	$("#spisak").css('height', $(window).height() - $("#filters").height() - $("#favoriti").height());
	// drugi nacin podesacanja css-a pomocu jQuery-ja. $(element).css(objekat_sa_osobinama);
	// objekat_sa_osobinama je dictionary u koji moze da se stavi vise osobina.
	detalji_css = { 'height' : $(window).height() - $("#filters").height() };
	$("#detalji").css(detalji_css);
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
	$("#prazan").load("/nekretnine/detalji?id_stana=" + objekat_id, function() {
		// initialize image slider when details are loaded
		if (window.isImageSliderLoaded) { // if slider was already loaded then only reload images
			window.imageSlider.reload();
		} else { // create slider if it is not yet loaded
			window.imageSlider = new mcImgSlider(window.sliderOptions);
			window.isImageSliderLoaded = true;
			window.imageSlider.reload();
		}
	});
	
}

function ucitajSpisakStanova() {
	var filter_dictionary = {};
	filters = $("#filters").find("[id^=filter_]").filter("[id$=_value]");
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

function dodajFiltere(filter_dict) {
	// pozvati $get kao u funkciji ucitajSpisakStanova, u filter_dictionary ubaciti promenljivu ime_filtera, a u view-u koji budes napravila treba da se napravi trazeni filter
	// u funkciji koja obradjuje odgovor od view-a pozvati append umesto html (html brise sve i stavlja ovo sto si joj dala, a append dodaje)
	var niz_filtera = [];
	for (filter in filter_dict) {
		niz_filtera.push(filter);
	}
	var filter_dictionary = {'niz_filtera': niz_filtera};
	$.get("/nekretnine/napravi_filtere", filter_dictionary, function (response) {
		$("#filters").append(response);
		for (filter in filter_dict) {
			window.prikazani_filteri[filter] = filter_dict[filter];
			$("#filter_" + filter + "_value").val(filter_dict[filter]).change(function(event){
				element = event.target;
				filter = element.id.substring(7, element.id.length-6);
				window.prikazani_filteri[filter] = $(element).val();
				$.cookie('filters', window.prikazani_filteri, {expires: 30});
			}).trigger("chosen:updated");
			if (filter != 'deo_grada') {
				$("#filter_" + filter + "_value").change();
			}
		}
		$.cookie('filters', window.prikazani_filteri, {expires: 30});
	});
}

function loadDependentFilter(dependent, depends_on_id) {
	filter_dictionary = {
		'filter_id': dependent,
		'depends_on_id': depends_on_id
	};
	$.get("/nekretnine/get_filter_content", filter_dictionary, function (response) {
		$("#filter_" + dependent + "_value").empty();
		$("#filter_" + dependent + "_value").html(response);
		$("#filter_" + dependent + "_value").val(window.prikazani_filteri[dependent])
		$("#filter_" + dependent + "_value").trigger('chosen:updated').change();
	});
}

function filter_depends_on(dependent, depends_on) {
	$("#filter_" + depends_on + "_value").change(function() {
		loadDependentFilter(dependent, $("#filter_" + depends_on + "_value").val());
	});
}