// animating boxes
$(function() {
	$('#talk-hover').click(function() {
	    talkSearch();
	});
	
	$('body').on('click','#talk-hover',function(){
	    $('#talk-hover').animate({
	        left: '340px'
	    },250);
	    $('#talk-main').animate({
	        left: '0px'
	    },250);
	    talkSearch();
	});

	$('body').on('mouseleave','#container',function(){
	    $('#talk-hover').animate({
	        left: '0px'
	    },250);
	    $('#talk-main').animate({
	        left: '-340px'
	    },250);
	});
});


function talkSearch() {
	var key = "d8gwb3us8jfcwbv85bm7qyj9";
	// var query = $('.taxonomy').text();
	var query = "religion and spirituality";
	var replaced = query.split(' ').join('+');
	var category = "talks";
	var url = "https://api.ted.com/v1/search.json?";
	var request = url+"q="+replaced+"&categories="+category+"&api-key="+key+"&externals=true&callback=?";
	$.getJSON(request, handleRequest);
}

function handleRequest(data) {
	// console.log(data.results);
	$('#ted-info').empty();
	for (var i=0; i < 10; i++) {
		var name = data.results[i].talk.name;
		var description = data.results[i].talk.description;
		var slug = data.results[i].talk.slug;
		var url = "http://www.ted.com/talks/"+slug;
		var one = "<div class='result'><h3 class='name'>";
		var two = "</h3><p class='description mini'>";
		var three = "</p><a href='";
		var four = "' target='_blank'>Click Here to View</a></div>";
		var output = one+name+two+description+three+url+four;
		document.getElementById('ted-info').innerHTML += output;
	}
}