// global vars section
var isMobileView = false;

$(document).ready(function(){

	// showing/hiding top menu
	$(document).on( "click", ".toggleMenuAction", function() {
		$(".nav_container").slideToggle();
	});

	if ($(window).width() <= 745) {
		isMobileView = true;
	}

	// TODO: if offset.top > 40px, then showing arrow up
});
