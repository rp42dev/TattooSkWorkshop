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
        setTimeout(function () {
        var textWidth = text.width();
        var fontSize = parseInt(text.css('font-size'));
        
        var newFontSize = Math.floor(fontSize * containerWidth / textWidth);
        console.log('new: ' + Math.floor(fontSize * containerWidth / textWidth), 'old: ' + fontSize, 'textWidth: ' + textWidth, 'containerWidth: ' + containerWidth, 'windowWidth: ' + windowWidth);
        text.css('font-size', newFontSize);
            clearTimeout($.data(this, 1000));
        }, 50);
    };

    $('.stretch ').stretch('.69rem');
    $('.heading').stretch('2.65rem');
    $(window).on('resize', function () {
        $('.stretch').stretch('.69rem');
        $('.heading').stretch('2.65rem');
    });
});
