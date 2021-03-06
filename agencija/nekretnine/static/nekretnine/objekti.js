(function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
(i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
})(window,document,'script','//www.google-analytics.com/analytics.js','ga');

ga('create', 'UA-64564624-1', 'auto');
ga('send', 'pageview');

var _SlideshowTransitions = [
	//Switch
	{ $Duration: 500, x: 0.25, $Zoom: 1.5, $Easing: { $Left: $JssorEasing$.$EaseInWave, $Zoom: $JssorEasing$.$EaseInSine }, $Opacity: 2, $ZIndex: -10, $Brother: { $Duration: 700, x: -0.25, $Zoom: 1.5, $Easing: { $Left: $JssorEasing$.$EaseInWave, $Zoom: $JssorEasing$.$EaseInSine }, $Opacity: 2, $ZIndex: -10 } }
];


window.imageSliderOptions = {
	$FillMode: 1,                                       //[Optional] The way to fill image in slide, 0 stretch, 1 contain (keep aspect ratio and put all inside slide), 2 cover (keep aspect ratio and cover whole slide), 4 actual size, 5 contain for large image, actual size for small image, default value is 0
	$DragOrientation: 3,                                //[Optional] Orientation to drag slide, 0 no drag, 1 horizental, 2 vertical, 3 either, default value is 1 (Note that the $DragOrientation should be the same as $PlayOrientation when $DisplayPieces is greater than 1, or parking position is not 0)
	$AutoPlay: true,                                    //[Optional] Whether to auto play, to enable slideshow, this option must be set to true, default value is false
	$AutoPlayInterval: 2500,                            //[Optional] Interval (in milliseconds) to go for next slide since the previous stopped if the slider is auto playing, default value is 3000
	$SlideshowOptions: {                                //[Optional] Options to specify and enable slideshow or not
		$Class: $JssorSlideshowRunner$,                 //[Required] Class to create instance of slideshow
		$Transitions: _SlideshowTransitions,            //[Required] An array of slideshow transitions to play slideshow
		$TransitionsOrder: 1,                           //[Optional] The way to choose transition to play slide, 1 Sequence, 0 Random
		$ShowLink: true                                    //[Optional] Whether to bring slide link on top of the slider when slideshow is running, default value is false
	},

	$BulletNavigatorOptions: {                                //[Optional] Options to specify and enable navigator or not
		$Class: $JssorBulletNavigator$,                       //[Required] Class to create navigator instance
		$ChanceToShow: 1,                               //[Required] 0 Never, 1 Mouse Over, 2 Always
		$AutoCenter: 1,                                 //[Optional] Auto center navigator in parent container, 0 None, 1 Horizontal, 2 Vertical, 3 Both, default value is 0
		$Steps: 1,                                      //[Optional] Steps to go for each navigation request, default value is 1
		$Lanes: 1,                                      //[Optional] Specify lanes to arrange items, default value is 1
		$SpacingX: 10,                                  //[Optional] Horizontal space between each item in pixel, default value is 0
		$SpacingY: 10,                                  //[Optional] Vertical space between each item in pixel, default value is 0
		$Orientation: 1                                 //[Optional] The orientation of the navigator, 1 horizontal, 2 vertical, default value is 1
	}
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
		var raw_city_parts = $("#city_parts").val()
		if (typeof raw_city_parts != 'undefined') {
			var city_parts = JSON.parse(raw_city_parts);
			startFilters = {deo_grada: city_parts};
		} else {
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

function setupObjectsPage() {
	$.cookie.json = true;
	window.favourites = $.cookie('favourites');
	if (typeof window.favourites != 'object') window.favourites = [];

	window.libFilter.initSlider();
	init_document_click();

	setHeightOfContainers();
	$(window).resize(setHeightOfContainers);

	window.libFilter.loadAvailableFilters(function() {
		window.libFilter.showFilters();
	});
}

function addToArray(ary, item) {
	var index = ary.indexOf(item);
	if (index == -1) {
		ary.push(item);
	}
}

function removeFromArray(ary, item) {
	var index = ary.indexOf(item);
	if (index > -1) {
		ary.splice(index, 1);
	}
}

function isFavourite(object_id) {
	var index = ary.indexOf(item);
	return index > -1;
}

function addFavourite(object_id) {
	if ($("#stan_" + object_id).parents("#spisak").length == 1) {
		x = $("#stan_" + object_id).remove();
		$("#favoriti").append(x);
		addToArray(window.favourites, object_id);
		ga('send', 'event', 'user_request', 'add', 'favourite');
		setFavouriteHeight();
	}
}

function removeFavourite(object_id) {
	if ($("#stan_" + object_id).parents("#favoriti").length == 1) {
		x = $("#stan_" + object_id).remove();
		$("#spisak").append(x);
		removeFromArray(window.favourites, object_id);
		ga('send', 'event', 'user_request', 'remove', 'favourite');
		setFavouriteHeight();
	}
}

function setFavouriteHeight() {
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
	$.cookie('favourites', window.favourites, {expires: 30});
}

function switchFavourite(object_id) {
	if ($("#stan_" + object_id).parents("#spisak").length == 1) {
		addFavourite(object_id);
	} else {
		removeFavourite(object_id);
	}
	setFavouriteHeight();
}

var heightTimeout = null;
function setHeightOfContainersDelayed() {
	if (heightTimeout) clearTimeout(heightTimeout);
	heightTimeout = setTimeout(setHeightOfContainers, 500);
}
function setHeightOfContainers() {
	// prvi nacin podesavanja css-a pomocu jQuery-ja. $(element).css(osobina, vrednost);
	$("#spisak").css('height', $(window).height() - $("#filters").height() - $("#favoriti").height() - $("#footer").height());
	// drugi nacin podesacanja css-a pomocu jQuery-ja. $(element).css(objekat_sa_osobinama);
	// objekat_sa_osobinama je dictionary u koji moze da se stavi vise osobina.
	detalji_css = { 'height' : $(window).height() - $("#filters").height() - $("#footer").height() };
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
	if (window.isImageSliderLoaded) $("#slider1_container").remove();
	$("#prazan").load("/detalji?id_stana=" + objekat_id, function() {
		// initialize image slider when details are loaded
		window.imageSlider = new $JssorSlider$("slider1_container", window.imageSliderOptions);
		window.isImageSliderLoaded = true;
		ga('send', 'event', 'site_response', 'show', 'details');
	});
	window.location.hash = objekat_id;
	ga('send', 'event', 'user_request', 'load', 'details');
}

var spisakStanovaTimeout = null;
function loadFlatList() {
	var filter_dictionary = {};
	var favourite_flats = [];
	Array.prototype.push.apply(favourite_flats, window.favourites);
	object_id = parseInt(window.location.hash.replace('#', ''), 10);
	if (!isNaN(object_id)) {
		// favourite_flats.push(object_id);
		vise(object_id);
	}

	filters = $("#filters").find("[id^=filter_]").filter("[id$=_value]");
	filters.each(function(index, element) {
		filter_id = element.id.substring(7, element.id.length-6);
		filter_value = $(element).val();
		if (filter_value != "0") {
			filter_dictionary[filter_id] = filter_value;
		}
		if (favourite_flats.length > 0) {
			filter_dictionary['favourite_flats'] = favourite_flats;
		}
	})
	$.get("/spisak", filter_dictionary, function (response) {
		$("#favoriti").html("");
		$("#spisak").html(response);
		for (index in favourite_flats) {
			addFavourite(favourite_flats[index]);
		}
	});
}
function ucitajSpisakStanova() {
	clearTimeout(spisakStanovaTimeout);
	spisakStanovaTimeout = setTimeout(loadFlatList, 500);
}

function report(object_id, report_type) {
	var params = {'object_id': object_id, 'my_token': window.getMyToken()}
	if (report_type == 'report_inactive' || report_type == 'report_middleman') {
		$.post("/" + report_type + "/", params).done(function (response) {
			$(".report_ad .button").hide();
			$("#thanksForReporting").show();
			ga('send', 'event', 'site_response', 'show', report_type + '_accepted');
		}).fail(function(response) {
			$("#reportingFailed").show();
			ga('send', 'event', 'site_response', 'show', report_type + '_failed');
		});
		ga('send', 'event', 'user_request', 'report', report_type);
	} else {
		ga('send', 'event', 'user_request', 'unknown_report', report_type);
	}
}

function send_message(object_id, name, phone, email, message) {
	message_text = 'Ime: ' + name + "\nTelefon: " + phone + "\nEmail: " + email + "\nPoruka: " + message;
	var params = {'object_id': object_id, 'message': message_text, 'my_token': window.getMyToken()}
	$.post("/send_message/", params).done(function(response) {
		$("#send_message_container").hide();
		$("#messageAccepted").show();
		ga('send', 'event', 'site_response', 'show', 'message_accepted');
	});
	ga('send', 'event', 'user_request', 'send_message');
}

function mouseover(){
	$("#filter_name").mouseover(function(){
        $("#filter_name").addClass("overmouse_color");
		});	
	}
$(mouseover);

