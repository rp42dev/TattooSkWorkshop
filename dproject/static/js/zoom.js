var scale = 1,
    panning = false,
    pointX = 0,
    pointY = 0,
    start = { x: 0, y: 0 },
    zooms = document.getElementsByClassName("zoom")

for (var i = 0; i < zooms.length; i++) {
    zoom = zooms[i];
    setTransform();

    function setTransform() {
        zoom.style.transform = "translate(" + pointX + "px, " + pointY + "px) scale(" + scale + ")";
    }

    console.log("zoom.js loaded", zoom);

    zoom.onmousedown = function (e) {
        e.preventDefault();
        start = { x: e.clientX - pointX, y: e.clientY - pointY };
        panning = true;
    }

    zoom.onmouseup = function (e) {
        panning = false;
    }

    zoom.onmousemove = function (e) {
        e.preventDefault();
        if (!panning) {
            return;
        }
        pointX = (e.clientX - start.x);
        pointY = (e.clientY - start.y);
        setTransform();
    }

    zoom.onwheel = function (e) {
        e.preventDefault();
        var xs = (e.clientX - pointX) / scale,
            ys = (e.clientY - pointY) / scale,
            delta = (e.wheelDelta ? e.wheelDelta : -e.deltaY);
        (delta > 0) ? (scale *= 1.2) : (scale /= 1.2);
        pointX = e.clientX - xs * scale;
        pointY = e.clientY - ys * scale;

        setTransform();
    }

    zoom.ontouchstart = function (e) {
        e.preventDefault();
        start = { x: e.touches[0].clientX - pointX, y: e.touches[0].clientY - pointY };
        panning = true;
    }

    zoom.ontouchend = function (e) {
        panning = false;
    }

    zoom.ontouchmove = function (e) {
        e.preventDefault();
        if (!panning) {
            return;
        }
        pointX = (e.touches[0].clientX - start.x);
        pointY = (e.touches[0].clientY - start.y);
        setTransform();
    }

    zoom.ontouchcancel = function (e) {
        panning = false;
    }

    zoom.ontouchleave = function (e) {
        panning = false;
    }

    zoom.ontouchenter = function (e) {
        panning = false;
    }

    zoom.ontouchend = function (e) {
        panning = false;
    }

    // detect pinch zoom
    zoom.addEventListener('touchstart', handleTouchStart, false);
    zoom.addEventListener('touchmove', handleTouchMove, false);

    var xDown = null;
    var yDown = null;

    function getTouches(evt) {
        return evt.touches ||             // browser API
            evt.originalEvent.touches; // jQuery
    }

    function handleTouchStart(evt) {
        const firstTouch = getTouches(evt)[0];
        xDown = firstTouch.clientX;
        yDown = firstTouch.clientY;
    }

    function handleTouchMove(evt) {
        if (!xDown || !yDown) {
            return;
        }

        var xUp = evt.touches[0].clientX;
        var yUp = evt.touches[0].clientY;

        var xDiff = xDown - xUp;
        var yDiff = yDown - yUp;

        if (Math.abs(xDiff) > Math.abs(yDiff)) {
            if (xDiff > 0) {
                /* left swipe */
            } else {
                /* right swipe */
            }
        } else {
            if (yDiff > 0) {
                /* up swipe */
                var xs = (evt.touches[0].clientX - pointX) / scale,
                    ys = (evt.touches[0].clientY - pointY) / scale,
                    delta = (evt.wheelDelta ? evt.wheelDelta : -evt.deltaY);
                (delta > 0) ? (scale *= 1.2) : (scale /= 1.2);
                pointX = evt.touches[0].clientX - xs * scale;
                pointY = evt.touches[0].clientY - ys * scale;

                setTransform();
            } else {
                /* down swipe */
                var xs = (evt.touches[0].clientX - pointX) / scale,
                    ys = (evt.touches[0].clientY - pointY) / scale,
                    delta = (evt.wheelDelta ? evt.wheelDelta : -evt.deltaY);
                (delta > 0) ? (scale *= 1.2) : (scale /= 1.2);
                pointX = evt.touches[0].clientX - xs * scale;
                pointY = evt.touches[0].clientY - ys * scale;

                setTransform();
            }
        }
        /* reset values */
        xDown = null;
        yDown = null;
    }



}

