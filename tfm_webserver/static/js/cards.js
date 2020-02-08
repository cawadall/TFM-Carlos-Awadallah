
$(document).ready(function () {
    $('#media').carousel({
        pause: true,
        interval: false,
    });
    $('[data-toggle="popover"]').popover({
        placement: 'right',
        trigger: 'hover',
        container: 'body'
    });
});

$(document).ready(function() {
    $('a.btn-simulation').click(function() {
        $('a.btn-simulation').addClass('disabled');
        $('#loader').removeClass('loaded')
    });
});