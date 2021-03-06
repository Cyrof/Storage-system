// code block to check if there is value in input and is matching else lock button
$('.passwd-int, .cfm-passwd-int').on('keyup', () => {
    if ($('.passwd-int').val() == $('.cfm-passwd-int').val()) {
        $('#msg').html('Matching').css('color', 'green');
        $('#sign-up-btn').prop('disabled', false);
    } else {
        $('#msg').html('Not Matching').css('color', 'red');
        $('#sign-up-btn').prop('disabled', true);
    }
});


// global code block to call popover class on bootstrap
$(function () {
    $('[data-toggle="popover"]').popover()
});

// function to set popover config
$("#pops").popover({
    html: true,
    content: function () {
        return $('.popover-para').html()
    }
})

// another code block to check if value in input email and confirm email are the same than unlock button
$('.rk-email-int, .cfm-email-int').on('keyup', () => {
    if ($('.rk-email-int').val() == $('.cfm-email-int').val()) {
        $('#rk-msg').html('Matching').css('color', 'green');
        $('#req-key-btn').prop('disabled', false);
    } else {
        $('#rk-msg').html('Not Matching').css('color', 'red')
        $('#req-key-btn').prop('disabled', true);
    }
});

// countdown to redirect function 
function countdown() {
    var time = 3;
    $('.redirect-text').html("<h3>Sign up successful</h3><br><p>Redirecting to log in page in<p id = 'redirect-text'></p></p>")
    const interval = setInterval(() =>{
        console.log(time);
        $('#redirect-text').html(time);
        time--;

        if (time < 0){
            clearInterval(interval);
            window.location.href='/';
        }
    }, 1000);
}

// function to write msg out 
function write_content(msg) {
    document.write(msg)
}

