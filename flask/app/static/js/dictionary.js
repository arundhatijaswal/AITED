// animating boxes
$(function() {
	$('#news-hover').on('mouseenter', function() {
		$('#news-hover').addClass('smaller');
		$('#news-hover p').animate({
	        opacity: '1'
	    },250);
	});
	$('#news-hover').on('mouseleave', function() {
		$('#news-hover').removeClass('smaller');
		$('#news-hover p').animate({
	        opacity: '0'
	    },250);
	});

	$('#dict-hover').on('mouseenter', function() {
		$('#dict-hover').addClass('smaller');
		$('#dict-hover p').animate({
	        opacity: '1'
	    },250);
	});
	$('#dict-hover').on('mouseleave', function() {
		$('#dict-hover').removeClass('smaller');
		$('#dict-hover p').animate({
	        opacity: '0'
	    },250);
	});

	$('#tts-hover').on('mouseenter', function() {
		$('#tts-hover').addClass('smaller');
		$('#tts-hover p').animate({
	        opacity: '1'
	    },250);
	});
	$('#tts-hover').on('mouseleave', function() {
		$('#tts-hover').removeClass('smaller');
		$('#tts-hover p').animate({
	        opacity: '0'
	    },250);
	});

	$('body').on('click','#dict-hover',function(){
	    $('#dict-hover').animate({
	        right: '0px'
	    },250);
	    $('#dict-main').animate({
	        right: '50px'
	    },250);
	    $('#dict-main').addClass('focus');
	});

	$('body').on('mouseleave','#container3',function(){
	    $('#dict-hover').animate({
	        right: '0px'
	    },250);
	    $('#dict-main').animate({
	        right: '-290px'
	    },250);
	    $('#dict-main').removeClass('focus');
	});

	$('#display').on('change', function(e) {
		// console.log('changed');
		$('#instructions').hide('slow');
		$('#dict-wrapper').hide();
		$('#output').hide();
		$('#sample').show();
	});

	$('#hide').on('change', function(e) {
		// console.log('changed');
		$('#instructions').show('slow');
		$('#dict-wrapper').show();
		splitText();
	});

	var min = "-150px", max = "0px";

    $('#show-panel').on('click', function(){
	    if ($("#dict-results").css("bottom") == min) {
	    	$("#dict-results").animate({ bottom: max }, 250);
	    	$("#show-panel").animate({ bottom: '150px' }, 250);
	    	$('#show-panel').addClass('up');
	    	$('#show-panel').removeClass('down');
	    }
	      
	    else {
	    	$("#dict-results").animate({ bottom: min }, 250);
	    	$("#show-panel").animate({ bottom: '0px' }, 250);
	    	$('#show-panel').addClass('down');
	    	$('#show-panel').removeClass('up');
	    }
	});
});


//FOR DICTIONARY
// to grab and split the text
function splitText() {
	var textString = $('#sample').text();
	console.log(textString);
	var splitString = textString.split(" ");
	$('#output').empty();
	$('#sample').hide();
	$('#output').show();
	for (var i = 0; i < splitString.length; i++) {
		$('#output').append(space(splitString[i]));	
	}
}

// to space out each string and make the word clickable
function space(word) {
	return "<span class='words' onclick='doubleTrouble(\"" + word + "\");'>" + word + "</span>";
}

// call the two search functions
function doubleTrouble(query) {
	if ($("#dict-results").css("bottom") == "-150px") {
    	$("#dict-results").animate({ bottom: "0px" }, 250);
    	$("#show-panel").animate({ bottom: '150px' }, 250);
    	$('#show-panel').addClass('up');
    	$('#show-panel').removeClass('down');
    }
    $('.words').click(function() {
    	$('.words').removeClass('highlighter');
		$(this).addClass('highlighter');
		search(query);
		search2(query);
	});
}

// make definition request to Google Dictionary
function search(query) {
	var key = "AiDwz6xRBaLzcYATfWuJC3jaSeC8hjwM";
	var q = query.toLowerCase().replace(/[^a-z0-9\s]/gi, ''); 
	var url = "https://api.pearson.com/v2/dictionaries/ldoce5/entries?search="+q+"&jsonp=data&apikey="+key;
	$.getJSON(url, handleRequest);
	$('#d-data').empty().append("<strong>Word: </strong><small class='query' id='q'>"+q+"</small>");
}

// get definitions
function handleRequest(data) {
	// console.log(data);
	for (var i = 0; i < data.results.length; i++) {
		var head = data.results[i].headword;
		// console.log(head);
		var search = $('#q').text();
		console.log(head, " ", search);
		if (head.toLowerCase() == search) {
			var pos = data.results[i].part_of_speech;
			var def = data.results[i].senses[0].definition;
			var def = data.results[i].senses[0].definition;
			$('#d-data').append("<p style='text-align:left;'><strong>Part of speech: </strong><small class='pos'>"+pos+"</small></p>");
			$('#d-data').append("<p style='text-align:left;'><strong>Definition: </strong><small class='def'>"+def+"</small></p>");
		}
		
		else {
			continue
		}
	}
}

//FOR THESAURUS
// make request to Big Huge Thesaurus
function search2(query) {
	var apiKey = "aqq3UFVvHqr7E7PSQki8";
	var q = query.toLowerCase().replace(/[^a-z0-9\s]/gi, ''); 
	var url = "http://thesaurus.altervista.org/thesaurus/v1?word=" + q + "&language=en_US&output=json&key=" + apiKey + "&callback=?";
	$.getJSON(url, carryoutRequest);
	$('#t-data').empty().append("<strong>Word: </strong><small class='query'>"+q+"</small>");
}

//get and print synonyms
function carryoutRequest(word) { 
  output = ""; 
  for (key in word.response) { 
    list = word.response[key].list; 
    output += list.synonyms;
  } 
  if (output)
		$('#t-data').append('<p><small>'+output+'</small></p>');
}



