$('.passwd-int, .cfm-passwd-int').on('keyup', () => {
    if ($('.passwd-int').val() == $('.cfm-passwd-int').val()) {
        $('#msg').html('Matching').css('color', 'green');
        $('#sign-up-btn').prop('disabled', false);
    } else {
        $('#msg').html('Not Matching').css('color', 'red');
        $('#sign-up-btn').prop('disabled', true);
    }
});
