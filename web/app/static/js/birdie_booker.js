const date = Date().toLocaleDateString;

$(function() {
  $( ".date-picker" ).datepicker({
      defaultDate: date
  });
});