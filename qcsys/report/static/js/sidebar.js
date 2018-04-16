var state = "expanded";
//Check if navbar is expanded or minimized and handle
$('#navbar-toggle').click(function() {
    if (state == "expanded") {
        $('.sidebar').css('margin-left', '-140px');
        $('#main_con').css('margin-left', '90px');
        $('#main_con').css('max-width', '1480px');
        state = "minimized";
    } else {
        if (state == "minimized") {
            $('.sidebar').css('margin-left', '0px');
            $('#main_con').css('margin-left', '220px');
            $('#main_con').css('max-width', '1280px');
            state = "expanded";
        }
    }
})


// Delete Modal pass parameter
$('#exampleModal').on('show.bs.modal', function (event) {
  var button = $(event.relatedTarget) // Button that triggered the modal
  var del_id = button.data('delid') // Extract info from data-* attributes
  //console.log(del_id)
  // If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
  // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
  var modal = $(this)
  urlStr = modal.find('#del_a').attr('href')
  modal.find('#del_a').attr('href', urlStr + del_id)
})

 //search box is empty
$('[name="search_form"]').submit(function(){
    var input = $.trim($('#labelsearch').val());
    if(input == ''){
        $('#labelsearch').val('');
         return false;
    }
});
