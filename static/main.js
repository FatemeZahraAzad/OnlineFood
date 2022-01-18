// const user_input = $("#user-input")
// const search_icon = $('#search-icon')
// const artists_div = $('#replaceable-content')
// const endpoint = '/artists/'
// const delay_by_in_ms = 700
// let scheduled_function = false
// console.log('bitch')
// let ajax_call = function (endpoint, request_parameters) {
// 	$.getJSON(endpoint, request_parameters)
// 		.done(response => {
// 			// fade out the artists_div, then:
// 			artists_div.fadeTo('slow', 0).promise().then(() => {
// 				// replace the HTML contents
// 				artists_div.html(response['html_from_view'])
// 				// fade-in the div with new contents
// 				artists_div.fadeTo('slow', 1)
// 				// stop animating search icon
// 				search_icon.removeClass('blink')
// 			})
// 		})
// }


// user_input.on('keyup', function () {

// 	const request_parameters = {
// 		q: $(this).val() // value of user_input: the HTML element with ID user-input
// 	}

// 	// start animating the search icon with the CSS class
// 	search_icon.addClass('blink')

// 	// if scheduled_function is NOT false, cancel the execution of the function
// 	if (scheduled_function) {
// 		clearTimeout(scheduled_function)
// 	}

// 	// setTimeout returns the ID of the function to be executed
// 	scheduled_function = setTimeout(ajax_call, delay_by_in_ms, endpoint, request_parameters)
// })


console.log('adding new address')
$(document).ready(function () {
	$("#add_new").submit(function (e) {
	  $('#AddAddressModal').modal().hide();
		e.preventDefault();
		var serializedData = $(this).serialize();
		console.log('sssssssss',serializedData)
		$.ajax({
			type: 'POST',
			url: "{% url 'check_out_post_address' %}",
			data: serializedData,
			success: function (response) {
				$('#AddAddressModal').modal().hide();
				$("#add_new").trigger('reset');
				$('#AddAddressModal').modal('hide');
				$('#address_list').html(response.data)
			},
			error: function (response) {
				alert(response["responseJSON"]["error"]);
			}
		})
	})
	
	$(".delete-item").click(function (e) {
		e.preventDefault();
		console.log(113333311)
		var _Pid = $(this).attr('data-item');
		console.log( _Pid)
		$.ajax({
		  url: "{% url 'delete_cart_item' %}",
		  data: {'pk':_Pid},
		  dataType:'json',
		  success: function (response) {
			  $('#cart_item_table').html(response.data)
			  console.log(response.data2)
			  $('#cart_len').html(response.data2)
		  },
		  error: function (response) {
			  alert(response["responseJSON"]["error"]);
		  }
	  })
	})  
})
