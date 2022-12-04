var scale = 1,
    panning = false,
    distance = 0,
    prevPositions = [],
    maxScale = 2.5,
    minScale = 0.6,
    threshold = 5,
    pointX = 0,
    pointY = 0,
    start = { x: 0, y: 0 },
    zoom = document.querySelector(".zoom");


function scaler(number, in_min, in_max, out_min, out_max) {
    return (number - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}

function setTransform() {
    zoom.style.transform = "translate(" + pointX + "px, " + pointY + "px) scale(" + scale + ")";
}

const reset = function () {
    scale = 1;
    pointX = 0;
    pointY = 0;
    setTransform();
}

const onMouseDown = function (e) {
    e.preventDefault();
    start = { x: e.clientX - pointX, y: e.clientY - pointY };
    panning = true;
}

const onMouseUp = function (e) {
    panning = false;
}

const onMouseMove = function (e) {
    e.preventDefault();
    if (!panning) {
        return;
    }
    pointX = (e.clientX - start.x);
    pointY = (e.clientY - start.y);
    setTransform();
}

const onZoom = function (e) {
    e.preventDefault();
    var xs = (e.clientX - pointX) / scale,
    ys = (e.clientY - pointY) / scale,
    delta = (e.wheelDelta ? e.wheelDelta : -e.deltaY);

    (delta > 0) ? ((maxScale > scale) && (scale *= 1.2)) : ((minScale < scale)&& (scale /= 1.2));

    pointX = e.clientX - xs * scale;
    pointY = e.clientY - ys * scale;
    setTransform();
}

const getDistance = function (e) {
    distance = Math.sqrt(Math.pow(e.touches[0].clientX - e.touches[1].clientX, 2) + Math.pow(e.touches[0].clientY - e.touches[1].clientY, 2));
    return distance;
}

const onTouchDown = function (e) {
    e.preventDefault();
    start = { x: e.touches[0].clientX - pointX, y: e.touches[0].clientY - pointY };
    panning = true;
}

const onTouchUp = function (e) {
    setTransform();
    prevPositions = [];
    panning = false;
}

const onPinchZoom = function (e) {
    e.preventDefault();
    if (e.touches.length != 2) return;
    panning = false;
    var currentDistance = getDistance(e);
    if (prevPositions.length > 0) {
        var prevDistance = prevPositions[0].distance;
        var diff = currentDistance - prevDistance;
        var xs = (e.touches[0].clientX - pointX) / scale,
            ys = (e.touches[0].clientY - pointY) / scale;
        if (Math.abs(diff) > threshold) {
            if (diff > 0) {
                (maxScale > scale) && (scale *= 1.02);
            } else {
                (minScale < scale) && (scale /= 1.02);
            }   
            pointX = e.touches[0].clientX - xs * scale;
            pointY = e.touches[0].clientY - ys * scale;
            setTransform();
            prevPositions = [];
        }
    }
    prevPositions.push({ distance: currentDistance });
    
}

const onMove = function (e) {
    e.preventDefault();
    if (e.touches.length == 2) {
        onPinchZoom(e);
    } else {
        if (!panning) {
            return;
        }
        pointX = (e.touches[0].clientX - start.x);
        pointY = (e.touches[0].clientY - start.y);
        setTransform();
    }
}

const loadPc = function () {
    setTransform();
    zoom.addEventListener("mousedown", onMouseDown);
    zoom.addEventListener("mouseup", onMouseUp);
    zoom.addEventListener("mousemove", onMouseMove);
    zoom.addEventListener("wheel", onZoom);
}

const loadMobile = function () {
    setTransform();
    zoom.addEventListener("touchmove", onMove);
    zoom.addEventListener("touchend", onTouchUp);
    zoom.addEventListener("touchstart", onTouchDown);
}

const clean = function () {
    zoom.removeEventListener("mousedown", onMouseDown);
    zoom.removeEventListener("mouseup", onMouseUp);
    zoom.removeEventListener("mousemove", onMouseMove);
    zoom.removeEventListener("wheel", onZoom);
    zoom.removeEventListener("touchmove", onMove);
    zoom.removeEventListener("touchend", onTouchUp);
    zoom.removeEventListener("touchstart", onTouchDown);
    reset();
}

const initZoom = function () {
    clean();
    zoom = document.querySelector('#zoom');
    if (window.matchMedia("(pointer: coarse)").matches) {
        loadMobile();
    } else {
        loadPc();
    }
}