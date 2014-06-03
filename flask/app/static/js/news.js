// animating boxes
$(function() {
	$('#news-hover').click(function() {
	    newsSearch();
	});
	

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


	$('body').on('click','#news-hover',function(){
	    $('#news-hover').animate({
	        right: '0px'
	    },250);
	    $('#news-main').animate({
	        right: '50px'
	    },250);
	    $('#news-main').addClass('focus');
	});

	$('body').on('mouseleave','#container2',function(){
	    $('#news-hover').animate({
	        right: '0px'
	    },250);
	    $('#news-main').animate({
	        right: '-290px'
	    },250);
	    $('#news-main').removeClass('focus');
	});
});

var key = "boX7CdYBW+zsr99xjmIB9Dt4W7vhViJu65816FiBPjg";

function newsSearch() {
	//Build up the URL for the request
	var maxresults = 15;
	var query = $('.category').text();
	console.log(query);
	var url = "https://api.datamarket.azure.com/Bing/Search/News?";
	var requestStr = url+"Query=%27"+query+"%27&$top="+maxresults+"&$format=json&Adult=%27Moderate%27&NewsSortBy=%27Date%27";
	
	//Return the promise from making an XMLHttpRequest to the server
	$.ajax({ 
		method:'GET',
		url: requestStr, 
		username: "",
		password:key,
		headers: {
        	"Authorization": "Basic " + base64_encode(":" + key)
    	},
		success: function(data, status) {
			$('#articles').empty();
			for (var i in data.d.results) {
				var title = data.d.results[i].Title;
				var source = data.d.results[i].Source;
				var link = data.d.results[i].Url;
				var snip = data.d.results[i].Description;
//				console.log(title);
//				console.log(source);
//				console.log(link);
				var output = "<div class='result'><span><a href="+link+" target='_blank'><h3 class='name'>"+ title +"</h3></a></span><p class='mini'>"+ source +"</p><p class='description'>"+ snip +"</p></div>";
				document.getElementById('articles').innerHTML += output;
			}
    	}
	})
}

function base64_encode(data) {
  // http://kevin.vanzonneveld.net
  // +   original by: Tyler Akins (http://rumkin.com)
  // +   improved by: Bayron Guevara
  // +   improved by: Thunder.m
  // +   improved by: Kevin van Zonneveld (http://kevin.vanzonneveld.net)
  // +   bugfixed by: Pellentesque Malesuada
  // +   improved by: Kevin van Zonneveld (http://kevin.vanzonneveld.net)
  // +   improved by: Rafal Kukawski (http://kukawski.pl)
  // *     example 1: base64_encode('Kevin van Zonneveld');
  // *     returns 1: 'S2V2aW4gdmFuIFpvbm5ldmVsZA=='
  // mozilla has this native
  // - but breaks in 2.0.0.12!
  //if (typeof this.window['btoa'] == 'function') {
  //    return btoa(data);
  //}
  var b64 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=";
  var o1, o2, o3, h1, h2, h3, h4, bits, i = 0,
    ac = 0,
    enc = "",
    tmp_arr = [];

  if (!data) {
    return data;
  }

  do { // pack three octets into four hexets
    o1 = data.charCodeAt(i++);
    o2 = data.charCodeAt(i++);
    o3 = data.charCodeAt(i++);

    bits = o1 << 16 | o2 << 8 | o3;

    h1 = bits >> 18 & 0x3f;
    h2 = bits >> 12 & 0x3f;
    h3 = bits >> 6 & 0x3f;
    h4 = bits & 0x3f;

    // use hexets to index into b64, and append result to encoded string
    tmp_arr[ac++] = b64.charAt(h1) + b64.charAt(h2) + b64.charAt(h3) + b64.charAt(h4);
  } while (i < data.length);

  enc = tmp_arr.join('');

  var r = data.length % 3;

  return (r ? enc.slice(0, r - 3) : enc) + '==='.slice(r || 3);

}