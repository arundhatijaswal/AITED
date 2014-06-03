$( document ).ready(function() {
    $('#topics').addClass("custom-select");
    $('#submit').addClass("btn btn-default");
});

// return similar ted talks based on the selected 
// topic; the user will be able to view and scroll
// through them


// animating boxes
$(function() {
	$('#talk-hover').click(function() {
	    talkSearch();
	});
	
	$('body').on('click','#talk-hover',function(){
	    $('#talk-hover').animate({
	        right: '0px'
	    },250);
	    $('#talk-main').animate({
	        right: '50px'
	    },250);
	    $('#talk-main').addClass('focus');
	    talkSearch();
	});

	$('body').on('mouseleave','#container',function(){
	    $('#talk-hover').animate({
	        right: '0px'
	    },250);
	    $('#talk-main').animate({
	        right: '-290px'
	    },250);
	    $('#talk-main').removeClass('focus');
	});
});


function talkSearch() {
	var key = "ptt5hg7vq2u2ebfzpvzxcedj";
	var query = $('.category').text();
	console.log(query);
	var category = "talks";
	var url = "https://api.ted.com/v1/search.json?";
	var request = url+"q="+query+"&categories="+category+"&api-key="+key+"&callback=?";
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
		var four = "' target='_blank' class='link'>Click Here to View</a></div>";
		var output = one+name+two+description+three+url+four;
		document.getElementById('ted-info').innerHTML += output;
	}
}




