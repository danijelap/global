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

function getObjectKeys(obj) {
	var keys = [];
	for(var key in obj){
		keys.push(key);
	}
	return keys;
}

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
			$("#filter_" + dependentFilterId + "_value").empty()
				.html(response)
				.val(window.libFilter.shownFilters[dependentFilterId])
				.trigger('chosen:updated').change();
		});
	},
	initSlider: function() {
		$("#filter_range_slider").slider({
			range: true,
			slide: function(event, ui) {
				$(window.active_filter_range + "_value").val( ui.values[ 0 ] + "-" + ui.values[ 1 ] );
			},
			stop: function(event, ui) {
				ucitajSpisakStanova();
			}
		});
	},
	addFilterChoice: function() {
		this.addFilterChoiceButtonClicked = true;
		var buttonPosition = $("#dugme_dodaj_filter").offset();
		var choicePosition = buttonPosition;
		choicePosition.left += 30;
		choicePosition.top += 25;
		
		var newFilters = $(getObjectKeys(window.libFilter.availableFilters)).not(getObjectKeys(window.libFilter.shownFilters)).get();
		var filter_dictionary = {'filters': newFilters};
		$.get('/nekretnine/get_filter_choice', filter_dictionary, function(response){
			$("#novi_filteri").show()
				.css(choicePosition)
				.html(response);
		});
		
	},
	removeFilter: function(id_filtera) {
		$("#filter_" + id_filtera).remove();
		delete window.libFilter.shownFilters[id_filtera];
		$.cookie('filters', window.libFilter.shownFilters, {expires: 30});
	}

};

$(function() {
	$.cookie.json = true;
	window.libFilter.initSlider();
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

function init_document_click(){
	window.libFilter.addFilterChoiceButtonClicked = false;
	$(document).click(function(){
		if (!window.libFilter.addFilterChoiceButtonClicked) {
			$("#novi_filteri").hide();
			$("#filter_range_slider").hide();
		}
		window.libFilter.addFilterChoiceButtonClicked = false;
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
