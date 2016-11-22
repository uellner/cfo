$(document).ready(function() {
  setProgressWidth(document);
});

$(document).on('shown.bs.modal', function(e) {
  setProgressWidth(e.target)
});

function setProgressWidth(context) {
  $('[role=progressbar]', context).each(
      function() {
        var that = this;
        $(that).width($(that).attr('aria-valuenow'));
  });
}
