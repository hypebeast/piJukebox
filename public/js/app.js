$(document).ready( function(){

  $('#start_playback').click(function() {

    // Send the birthday date and receive the answer
    $.ajax({
      url: "/start",
      success: function(data) {
        
      }
    });
  });

  $('#stop_playback').click(function(ev) {
    ev.preventDefault();

    // Send the birthday date and receive the answer
    $.ajax({
      url: "/stop",
      success: function(data) {
        
      }
    });
  });

});