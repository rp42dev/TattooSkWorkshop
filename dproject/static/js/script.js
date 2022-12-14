

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

