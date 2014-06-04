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

	$('input:radio[name="tts"]').change( function() {
		
		if ($(this).val() == 'talk-off') {
			$('#myModal').modal('hide');
		}

		else if($(this).val() == 'talk-on') {
			$('#myModal').modal('show');
			vh_sceneLoaded();
		}
	});
	
	$('#myModal').on('hidden.bs.modal', function (e) {
		$("input[name='tts'][value='talk-off']").prop('checked', true);
	})
});


function vh_sceneLoaded(){
	// readScript();
    var text = $('.part1').text();
    console.log(text);
    // var text = "Hello. Welcome.";
	//the scene begins playing, add actions here
	// sayText(text, voice, lang ID, family ID)
    sayText(text,3,1,4); 
}

// function readScript() {
	
// }