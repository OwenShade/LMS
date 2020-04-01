const search = $("#search")
const option = $('#options')
const results_div = $('#dynamic_content')
const endpoint = '/LMS/search/'
const delay_by_in_ms = 700
let scheduled_function = false

let ajax_call = function (endpoint, request_parameters) {
	$.getJSON(endpoint, request_parameters)
		.done(response => {
			// fade out the artists_div, then:
			results_div.fadeTo('slow', 0).promise().then(() => {
				// replace the HTML contents
				results_div.html(response['html_from_view'])
				// fade-in the div with new contents
				results_div.fadeTo('slow', 1)
			})
		})
}

let execute = function () {

	const request_parameters = {
        search: $(this).val(),
        options: $(option).val()
    }

	// if scheduled_function is NOT false, cancel the execution of the function
	if (scheduled_function) {
		clearTimeout(scheduled_function)
	}

	// setTimeout returns the ID of the function to be executed
	scheduled_function = setTimeout(ajax_call, delay_by_in_ms, endpoint, request_parameters)
}

search.on('keyup',execute)