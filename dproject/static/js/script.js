
// show Toast when message is sent
$(document).ready(function () {
    $(".toast").toast("show");
    $('.back').on('click', function (e) {
        e.preventDefault();
        window.history.back();
    });

});

// stretch text to fit container
$((function () {
    $.fn.stretch = function (init) {
        var text = $(this);
        text.css('font-size', init);
        var textWidth = text.width();
        var containerWidth = $('.masthead-content').width();
        var fontSize = parseInt(text.css('font-size'));

        var newFontSize = Math.floor(fontSize * containerWidth / textWidth);
        text.css('font-size', newFontSize);
        clearTimeout($.data(this, 1000));
    };
}));

$(window).on('resize', function () {
    $('.stretch').stretch ('.70rem');
    $('.heading').stretch ('2rem');
});

$('.masthead').ready(function () {
    if ($(".masthead")[0]) {
        $('#video').get(0).play();
    }
    $('.stretch ').stretch ('.70rem');
    $('.heading').stretch ('2rem');
});


// Lazy load images
$(window).on("load", function () {
    $(window).scroll(function () {
        var windowBottom = $(this).scrollTop() + $(this).innerHeight();
        $(".fade").each(function () {
            var objectBottom = $(this).offset().top + 50;
            if (objectBottom < windowBottom) { 
                $(this).removeClass('fade');
            }
        });
        
    }).scroll();
});

// form validation
(function () {
    'use strict'
    var forms = document.querySelectorAll('.needs-validation')
    Array.prototype.slice.call(forms)
        .forEach(function (form) {
            form.addEventListener('submit', function (event) {
                if (!form.checkValidity()) {
                    event.preventDefault()
                    event.stopPropagation()
                }

                form.classList.add('was-validated')
            }, false)
        })
})();



