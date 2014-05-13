$( document ).ready(function() {
    $('#topics').addClass("custom-select");
    $('#submit').addClass("btn btn-default");
});

function checkFirstVisit() {
  if(document.cookie.indexOf('mycookie')==-1) {
    // cookie doesn't exist, create it now
    document.cookie = 'mycookie=1';
  }
  else {
    transition(); 
  }
}

function transition() {
	setTimeout( "jQuery('.header').addClass('header-shrink');", 2000 );
    setTimeout( "jQuery('#front').addClass('transitioned shadow').css({'padding':'0'});", 1400 );
  	setTimeout( "jQuery('.sub-header').hide();", 2000 );
  	setTimeout( "jQuery('form').removeClass('form-horizontal').addClass('form-inline');", 2000 );
  	setTimeout( "jQuery('div').removeClass('button');", 2000 );
  	setTimeout( "jQuery('.select-style').css({'float':'left', 'width':'65%', 'margin-left':'15%', 'margin-right':'10px'});", 2000 );
}