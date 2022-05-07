// function to make nav responsive
let expandcollapse = () => {
    if ($(window).width() < 900) {
        $(() => {
            // add class collapse to nav-tab
            let tab = $('.nav-tab');
            tab.addClass('collapse');
            // change css element for button
            $('.btn1').show();
        });
    }
    else if ($(window).width() >= 900) {
        $(() => {
            // class collapse from nav-tab
            let tab = $('.nav-tab');
            tab.removeClass('collapse');
            tab.removeClass('show');
            $('.nav-list').css('flex-direction', 'row');
            // change css elememt for button
            $('.btn1').hide();
        })
    }
}

// browse button function
let nav_toggle = $('.btn1').on('click', () => {
    if (!$('.nav-tab').hasClass('show')) {
        $(() => {
            let table = $('.nav-list');
            table.css('flex-direction', 'column');
        });
    }
});

$(window).on('load', expandcollapse);
$(window).on('resize', expandcollapse);
$(document).on('ready', () => {
    $(window).on('resize', expandcollapse);
});
