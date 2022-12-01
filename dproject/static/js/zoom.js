var scale = 1,
    panning = false,
    pointX = 0,
    pointY = 0,
    start = { x: 0, y: 0 },
    zooms = document.getElementsByClassName("zoom")

console.log(zooms)

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

}

