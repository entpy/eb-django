$(document).ready(function(){

	// loading default block serivces
	load_default_services_block();

	// fancybox init
	$(".fancybox").fancybox({
		"openEffect" : "none"
	});

	$(".serviceClickAction").on("click",  function(){

		var blockNumberResult = false;
		var blockNumber = false;

		$(".serviceNameAction").removeClass("service_active");
		$(this).addClass("service_active");
		// retrieving current block number
		blockNumberResult = $(this).attr("class").match(/@@([^@]+)@@/);
		blockNumber = blockNumberResult[1];

		load_services_block(blockNumber);

		// vertical scolling to this element
		if (isMobileView) {
			$("html").scrollTop($(this).offset().top);
		}

		return true;
	});

	function load_default_services_block() {
		load_services_block(1);

		return true;
	}

	function load_services_block(blockNumber) {
		if (blockNumber) {
			$(".service_html_container").html($(".html_block_service_" + blockNumber).html());
		}

		return true;
	}
});
