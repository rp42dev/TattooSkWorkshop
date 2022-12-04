
// show Toast when message is sent
$(document).ready(function () {
    $(".toast").toast("show");
    $('.back').on('click', function (e) {
        e.preventDefault();
        window.history.back();
    });

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



