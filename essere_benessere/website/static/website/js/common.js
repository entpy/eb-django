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

function placeholder_support() {
	Modernizr.load({
		test: Modernizr.input.placeholder,
		nope: ['/static/website/js/jquery.placeholder.js'],
		complete: function(){
			if (!Modernizr.input.placeholder) {
				$('input, textarea').placeholder();
			}
		}
	});

	return true;
}
