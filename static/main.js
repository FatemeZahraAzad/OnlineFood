

// console.log('adding new address')
// $(document).ready(function () {
// 	$("#add_new").submit(function (e) {
// 	  $('#AddAddressModal').modal().hide();
// 		e.preventDefault();
// 		var serializedData = $(this).serialize();
// 		console.log('sssssssss',serializedData)
// 		$.ajax({
// 			type: 'POST',
// 			url: "{% url 'check_out_post_address' %}",
// 			data: serializedData,
// 			success: function (response) {
// 				$('#AddAddressModal').modal().hide();
// 				$("#add_new").trigger('reset');
// 				$('#AddAddressModal').modal('hide');
// 				$('#address_list').html(response.data)
// 			},
// 			error: function (response) {
// 				alert(response["responseJSON"]["error"]);
// 			}
// 		})
// 	})
	
// 	$(".delete-item").click(function (e) {
// 		e.preventDefault();
// 		console.log(113333311)
// 		var _Pid = $(this).attr('data-item');
// 		console.log( _Pid)
// 		$.ajax({
// 		  url: "{% url 'delete_cart_item' %}",
// 		  data: {'pk':_Pid},
// 		  dataType:'json',
// 		  success: function (response) {
// 			  $('#cart_item_table').html(response.data)
// 			  console.log(response.data2)
// 			  $('#cart_len').html(response.data2)
// 		  },
// 		  error: function (response) {
// 			  alert(response["responseJSON"]["error"]);
// 		  }
// 	  })
// 	})  
// })
