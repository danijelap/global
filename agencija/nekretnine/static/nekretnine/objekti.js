(function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
(i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
})(window,document,'script','//www.google-analytics.com/analytics.js','ga');

ga('create', 'UA-64564624-1', 'auto');
ga('send', 'pageview');

window.sliderOptions=
{
	sliderId: "slider",
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
	m: false
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
		$.get("/get_filter_list/", function (response) {
			window.libFilter.availableFilters = response;
			window.libFilter.shownFilters = {};
			onComplete();
		}, 'json');
		ga('send', 'event', 'user_request', 'load', 'filters');
	},
	showFilters: function() {
		startFilters = $.cookie('filters');
		if (typeof startFilters === 'undefined') {
			startFilters = {};
			for (filter_id in this.availableFilters) {
				if (this.availableFilters[filter_id]['default']) {
					if (this.availableFilters[filter_id]['start_value']) {
						startFilters[filter_id] = this.availableFilters[filter_id]['start_value'];
					} else {
						startFilters[filter_id] = 0;
					}
				}
			}
		}
		this.appendFilters(startFilters);

		ga('send', 'event', 'site_response', 'show', 'filters', getObjectKeys(startFilters).length);
	},
	appendFilters: function(filterDictionary) {
		var filterArray = [];
		for (var filter_id in filterDictionary) {
			filterArray.push(filter_id);
		}
		$.get("/make_filters/", {'filter_array': filterArray}, function (response) {
			$("#filters").append(response);
			for (var filter_id in filterDictionary) {
				window.libFilter.shownFilters[filter_id] = filterDictionary[filter_id];
				$("#filter_" + filter_id + "_value").val(filterDictionary[filter_id]).change(function(event){
					var element = event.target;
					var filter_id = element.id.substring(7, element.id.length - 6);
					window.libFilter.shownFilters[filter_id] = $(element).val();
					$.cookie('filters', window.libFilter.shownFilters, {expires: 30});
				});
				var dependsOnFilterId = window.libFilter.availableFilters[filter_id]['depends_on'];
				if (dependsOnFilterId) {
					if (dependsOnFilterId in window.libFilter.shownFilters) {
						$("#filter_" + dependsOnFilterId + "_value").change(window.libFilter.dependsOnFilterChange);
						dependsOnFilterValue = $("#filter_" + dependsOnFilterId + "_value").val()
						window.libFilter.loadDependentFilter(filter_id, dependsOnFilterValue);
					}
				} else {
					if (window.libFilter.getDependentFilter(filter_id)) {
						var dependentFilterId = window.libFilter.getDependentFilter(filter_id);
						$("#filter_" + filter_id + "_value").change(window.libFilter.dependsOnFilterChange);
					}
					if ($("#filter_" + filter_id + "_value")[0].sumo) {
						$("#filter_" + filter_id + "_value")[0].sumo.reload();
					}
					$("#filter_" + filter_id + "_value").change();
				}
			}
			$.cookie('filters', window.libFilter.shownFilters, {expires: 30});
			ga('send', 'event', 'site_response', 'show', 'new_filters', getObjectKeys(filterDictionary).length);
		});
	},
	dependsOnFilterChange: function(event) {
		// TODO
		dependsOnFilterElement = event.target;
		dependsOnFilterId = dependsOnFilterElement.id.substring(7, dependsOnFilterElement.id.length - 6);
		dependentFilterId = window.libFilter.getDependentFilter(dependsOnFilterId);
		dependsOnFilterValue = $(dependsOnFilterElement).val();
		window.libFilter.loadDependentFilter(dependentFilterId, dependsOnFilterValue);
	},
	getDependentFilter: function(dependsOnFilterId) {
		for (var filter_id in window.libFilter.availableFilters) {
			if (window.libFilter.availableFilters[filter_id]['depends_on'] == dependsOnFilterId) {
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
		$.get("/get_filter_content", filterDictionary, function (response) {
			$("#filter_" + dependentFilterId + "_value").empty()
				.html(response)
				.val(window.libFilter.shownFilters[dependentFilterId]);
			$("#filter_" + dependentFilterId + "_value")[0].sumo.reload();
			$("#filter_" + dependentFilterId + "_value").change();
		});
	},
	initSlider: function() {
		$("#filter_range_slider").slider({
			range: true,
			slide: function(event, ui) {
				$("#filter_" + window.libFilter.activeFilterRange + "_value").val(ui.values[ 0 ] + "-" + ui.values[ 1 ]);
			},
			stop: function(event, ui) {
				ucitajSpisakStanova();
				window.libFilter.shownFilters[window.libFilter.activeFilterRange] = ui.values[ 0 ] + "-" + ui.values[ 1 ];
				$.cookie('filters', window.libFilter.shownFilters, {expires: 30});
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
		$.get('/get_filter_choice', filter_dictionary, function(response){
			$("#new_filters").show()
				.css(choicePosition)
				.html(response);
		});
		
	},
	removeFilter: function(id_filtera) {
		$("#filter_" + id_filtera).remove();
		delete window.libFilter.shownFilters[id_filtera];
		$.cookie('filters', window.libFilter.shownFilters, {expires: 30});
		ga('send', 'event', 'user_request', 'remove', 'filter');
	},
	initFilterSlider: function(slider_id) {
		jq_filter_slider_id = "#" + slider_id;
		$(jq_filter_slider_id).mouseover(function(event){
			filter_id = '#' + this.id;
			var filter_position = $(filter_id).offset();
			var new_slider_position = filter_position;
			new_slider_position.top += 25;
			$("#filter_range_slider").slider( "option", "max", parseFloat($(filter_id + "_max").val()));
			$("#filter_range_slider").slider( "option", "min", parseFloat($(filter_id + "_min").val()));
			$("#filter_range_slider").slider( "option", "values", $(filter_id + "_value").val().split('-'));
			$("#filter_range_slider").show().css(new_slider_position);
			window.libFilter.activeFilterRange = this.id.substring(7, this.id.length);
		});
	}


};

window.getMyToken = function() {
	var mytoken = $.cookie('mytoken');
	if (typeof mytoken === 'undefined') {
		mytoken = Math.floor(Math.random() * 100000000); 
		$.cookie('mytoken', mytoken, {expires: 365});
	}
	return mytoken;
}
var csrftoken = $.cookie('csrftoken');
function csrfSafeMethod(method) {
	// these HTTP methods do not require CSRF protection
	return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
	beforeSend: function(xhr, settings) {
		if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
			xhr.setRequestHeader("X-CSRFToken", csrftoken);
		}
	}
});

$(function() {
	$.cookie.json = true;
	window.libFilter.initSlider();
	init_document_click();
	
	setHeightOfContainers();
	$(window).resize(setHeightOfContainers);
	
	window.libFilter.loadAvailableFilters(function() {
		window.libFilter.showFilters();
//		ucitajSpisakStanova();
	});
	
});

function add_favorits(id_objekta) {
	if ($("#stan_" + id_objekta).parents("#spisak").length == 1) {
		x = $("#stan_" + id_objekta).remove();
		$("#favoriti").append(x);
		ga('send', 'event', 'user_request', 'add', 'favourite');
	} else {
		x = $("#stan_" + id_objekta).remove();
		$("#spisak").append(x);
		ga('send', 'event', 'user_request', 'remove', 'favourite');
	}
	favoriti = $("#favoriti").find("[id^=stan_]");
	favorites_total_height = 0;
	favoriti.each(function(index, element){
		favorites_total_height += $(element).outerHeight(true);
	});
	if (favorites_total_height > 0) favorites_total_height += 2;
	maximum_height = 200
	if (favorites_total_height <= maximum_height) {
		$("#favoriti").css('height', favorites_total_height);
	} else {
		$("#favoriti").css('height', maximum_height);
	}
	setHeightOfContainers();
}

var heightTimeout = null;
function setHeightOfContainersDelayed() {
	if (heightTimeout) clearTimeout(heightTimeout);
	heightTimeout = setTimeout(setHeightOfContainers, 500);
}
function setHeightOfContainers() {
	// prvi nacin podesavanja css-a pomocu jQuery-ja. $(element).css(osobina, vrednost);
	$("#spisak").css('height', $(window).height() - $("#filters").height() - $("#favoriti").height());
	// drugi nacin podesacanja css-a pomocu jQuery-ja. $(element).css(objekat_sa_osobinama);
	// objekat_sa_osobinama je dictionary u koji moze da se stavi vise osobina.
	detalji_css = { 'height' : $(window).height() - $("#filters").height() };
	$("#right").css(detalji_css);
}

function init_document_click(){
	window.libFilter.addFilterChoiceButtonClicked = false;
	$(document).click(function(){
		if (!window.libFilter.addFilterChoiceButtonClicked) {
			$("#new_filters").hide();
			$("#filter_range_slider").hide();
		}
		window.libFilter.addFilterChoiceButtonClicked = false;
	});
}

function vise(objekat_id) {
	$("#prazan").load("/detalji?id_stana=" + objekat_id, function() {
		// initialize image slider when details are loaded
		if (window.isImageSliderLoaded) { // if slider was already loaded then only reload images
			window.imageSlider.reload();
		} else { // create slider if it is not yet loaded
			window.imageSlider = new mcImgSlider(window.sliderOptions);
			window.isImageSliderLoaded = true;
			window.imageSlider.reload();
		}
		ga('send', 'event', 'site_response', 'show', 'details');
	});
	
	ga('send', 'event', 'user_request', 'load', 'details');
}

function ucitajSpisakStanova() {
	// TODO: add delay
	var filter_dictionary = {};
	filters = $("#filters").find("[id^=filter_]").filter("[id$=_value]");
	filters.each(function(index, element) {
		filter_id = element.id.substring(7, element.id.length-6);
		filter_value = $(element).val();
		if (filter_value != "0") {
			filter_dictionary[filter_id] = filter_value;
		}
	})
	$.get("/spisak", filter_dictionary, function (response) {
		$("#spisak").html(response);
	});
}

function reportInactive(object_id) {
	params = {'object_id': object_id, 'my_token': window.getMyToken()}
	$.post("/report_inactive/", params).done(function (response) {
		$("#reportingButton").hide();
		$("#thanksForReporting").show();
		ga('send', 'event', 'site_response', 'show', 'report_inactive_accepted');
	}).fail(function(response) {
		$("#reportingFailed").show();
		ga('send', 'event', 'site_response', 'show', 'report_inactive_failed');
	});
	ga('send', 'event', 'user_request', 'report', 'inactive');
}
function mouseover(){
	$("#filter_name").mouseover(function(){
        $("#filter_name").addClass("overmouse_color");
		});	
	}
$(mouseover);

