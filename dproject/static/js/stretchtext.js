// stretch text to fit container

$(document).ready(function () {
    $.fn.stretch = function (init) {
        var text = $(this);
        text.css('font-size', init);
        var containerWidth = $('.masthead-content').width();
        var windowWidth = $(window).width();
        if (windowWidth < 1920) {
            containerWidth = windowWidth;
        } else {
            containerWidth = 1920;
        }

        var textWidth = text.width();
        var fontSize = parseInt(text.css('font-size'));

        var newFontSize = Math.floor(fontSize * containerWidth / textWidth);
        text.css('font-size', newFontSize);
        clearTimeout($.data(this, 1000));

    };
    setTimeout(function () {
        $('.stretch ').stretch('.69rem');
        $('.heading').stretch('2.65rem');
        $('.heading2').stretch('2.80rem');
        $(window).on('resize', function () {

            $('.stretch').stretch('.69rem');
            $('.heading').stretch('2.65rem');
            $('.heading2').stretch('2.80rem');

        });
    }, 150);
}); 
