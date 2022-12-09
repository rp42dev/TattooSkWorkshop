// stretch text to fit container

$(document).ready(function () {
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

    $('.stretch ').stretch('.70rem');
    $('.heading').stretch('2rem');
    $(window).on('resize', function () {
        $('.stretch').stretch('.70rem');
        $('.heading').stretch('2rem');
    });
});
