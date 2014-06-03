// animating boxes
$(function() {
	// $('#talk-hover').click(function() {
	//     talkSearch();
	// });
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

	
	$('body').on('click','#tts-hover',function(){
	    $('#tts-hover').animate({
	        right: '0px'
	    },250);
	    $('#tts-main').animate({
	        right: '50px'
	    },250);
	    $('#tts-main').addClass('focus');
	});

	$('body').on('mouseleave','#container4',function(){
	    $('#tts-hover').animate({
	        right: '0px'
	    },250);
	    $('#tts-main').animate({
	        right: '-290px'
	    },250);
	    $('#tts-main').removeClass('focus');
	});

	$('#talk-off').on('change', function(e) {
		$('#myModal').modal('hide');
	});

	$('#talk-on').on('change', function(e) {
		$('#myModal').modal('show');
		vh_sceneLoaded();
	});
});


function vh_sceneLoaded(){
    // var text = $('.part1').text();
    // console.log(text);
    var text = "Hello. Welcome.";
    //the scene begins playing, add actions here
    sayText(text,1,1,3); 
}