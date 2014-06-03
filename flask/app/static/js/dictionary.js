// animating boxes
$(function() {
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



	$('input:radio[name="readmode"]').change( function() {
		
		if ($(this).val() == 'display') {
			$('#instructions').show('slow');
			$('#dict-wrapper').show();
			splitText();
		}

		else if($(this).val() == 'hide') {
			$('#instructions').hide('slow');
			$('#dict-wrapper').hide();

			$('.d-thesis').hide();
			$('.d-import').hide();
			$('.d-chal').hide();
			$('.d-soln').hide();
			$('.d-impact').hide();
			$('.d-quote').hide();

			$('.part1').show();
			$('.part2').show();
			$('.part3').show();
			$('.part4').show();
			$('.part5').show();
			$('.part6').show();
		}
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
function splitText(text) {
	var one = $('.part1').text().split(" ");
	var two = $('.part2').text().split(" ");
	var three = $('.part3').text().split(" ");
	var four = $('.part4').text().split(" ");
	var five = $('.part5').text().split(" ");
	var six = $('.part6').text().split(" ");
	// console.log(one);

	$('.d-thesis').empty();
	$('.d-import').empty();
	$('.d-chal').empty();
	$('.d-soln').empty();
	$('.d-impact').empty();
	$('.d-quote').empty();

	$('.part1').hide();
	$('.part2').hide();
	$('.part3').hide();
	$('.part4').hide();
	$('.part5').hide();
	$('.part6').hide();

	$('.d-thesis').show();
	$('.d-import').show();
	$('.d-chal').show();
	$('.d-soln').show();
	$('.d-impact').show();
	$('.d-quote').show();

	for (var i = 0; i < one.length; i++) {
		$('.d-thesis').append(space(one[i]));	
	}

	for (var i = 0; i < two.length; i++) {
		$('.d-import').append(space(two[i]));	
	}

	for (var i = 0; i < three.length; i++) {
		$('.d-chal').append(space(three[i]));	
	}

	for (var i = 0; i < four.length; i++) {
		$('.d-soln').append(space(four[i]));	
	}

	for (var i = 0; i < five.length; i++) {
		$('.d-impact').append(space(five[i]));	
	}

	for (var i = 0; i < six.length; i++) {
		$('.d-quote').append(space(six[i]));	
	}
}

// to space out each string and make the word clickable
function space(word) {
	return "<span class='words' onclick='doubleTrouble(\"" + word + "\");'>" + word + "</span>";
}

// call the two search functions
function doubleTrouble(query) {
	// $(this).addClass('highlighter');
	$('.words').click(function() {
		$('.words').removeClass('highlighter');
		$(this).addClass('highlighter');
		var words = $(this).text();
		// console.log(words);
		// doubleTrouble(words);
	});

	if ($("#dict-results").css("bottom") == "-150px") {
    	$("#dict-results").animate({ bottom: "0px" }, 250);
    	$("#show-panel").animate({ bottom: '150px' }, 250);
    	$('#show-panel').addClass('up');
    	$('#show-panel').removeClass('down');
    }
    search_dict(query);
	search2(query);
}

// make definition request to Google Dictionary
function search_dict(query) {
	var key = "AiDwz6xRBaLzcYATfWuJC3jaSeC8hjwM";
	var q = query.toLowerCase().replace(/[^a-z0-9\s]/gi, ''); 
	var url = "https://api.pearson.com/v2/dictionaries/ldoce5/entries?search="+q+"&jsonp=data&apikey="+key;
	$.getJSON(url, request);
	$('#d-data').empty().append("<strong>Word: </strong><small class='query' id='q'>"+q+"</small>");
}

// get definitions
function request(data) {
	console.log(data);
	var search = $('#q').text();
	// search2(search);

	for (var i = 0; i < data.results.length; i++) {
		var head = data.results[i].headword;
		// console.log(head);
		// console.log(head, " ", search);
		if (head.toLowerCase() == search) {
			var pos = data.results[i].part_of_speech;
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
	var output = ""; 
	console.log(word);

	for (var i=0; i<2; i++) { 
		var key = word.response[i].list.synonyms; 
		var data = "<p>"+key+"</p>";
		output += data;
	} 

	if (output != "") {
		$('#t-data').append('<p><small>'+output+'</small></p>');
	}

	else {
		$('#t-data').append('<p><small>No Results</small></p>');
	}
		
}



