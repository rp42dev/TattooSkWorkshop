
// show Toast when message is sent
$(document).ready(function () {
    $(".toast").toast("show");
});

// fade i on scroll events
$(window).on("load", function () {

    $(window).scroll(function () {
        var windowBottom = $(this).scrollTop() + $(this).innerHeight();
        $(".fade").each(function () {
            /* Check the location of each desired element */
            var objectBottom = $(this).offset().top + 50;

            /* If the element is completely within bounds of the window, fade it in */
            if (objectBottom < windowBottom) { //object comes into view (scrolling down)
                if ($(this).css("opacity") == 0) { $(this).fadeTo(250, 1); }
            } else { //object goes out of view (scrolling up)
                if ($(this).css("opacity") == 1) { $(this).fadeTo(250, 0); }
            }
        });
    }).scroll(); //invoke scroll-handler on page-load
});

// form validation
(function () {
    'use strict'
    // Fetch all the forms we want to apply custom Bootstrap validation styles to
    var forms = document.querySelectorAll('.needs-validation')

    // Loop over them and prevent submission
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
})()


