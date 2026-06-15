(function () {
    let scale = 1;
    let pointX = 0;
    let pointY = 0;
    let startX = 0;
    let startY = 0;
    let panning = false;
    let prevDistance = 0;
    let zoomTarget = null;
    let imgElement = null;
    let lastTap = 0;

    const maxScale = 4.0;
    const minScale = 1.0;

    function init() {
        zoomTarget = document.querySelector("#zoom");
        if (!zoomTarget) return;

        imgElement = zoomTarget.querySelector("img");
        if (!imgElement) return;

        // Reset positions
        scale = 1;
        pointX = 0;
        pointY = 0;
        updateTransform(false);

        // Remove any old event listeners (clean state)
        destroy();

        // PC Listeners
        zoomTarget.addEventListener("mousedown", onMouseDown);
        window.addEventListener("mousemove", onMouseMove);
        window.addEventListener("mouseup", onMouseUp);
        zoomTarget.addEventListener("wheel", onWheel, { passive: false });
        zoomTarget.addEventListener("dblclick", onDoubleClick);

        // Mobile Listeners
        zoomTarget.addEventListener("touchstart", onTouchStart, { passive: false });
        zoomTarget.addEventListener("touchmove", onTouchMove, { passive: false });
        zoomTarget.addEventListener("touchend", onTouchEnd);

        // Keyboard navigation
        window.addEventListener("keydown", onKeyDown);

        // First-time tutorial overlay logic
        initTutorial();
    }

    function initTutorial() {
        const tutorial = document.querySelector("#zoom-tutorial");
        if (!tutorial) return;

        const tutorialSeen = localStorage.getItem("zoom_tutorial_seen");
        if (!tutorialSeen) {
            // Show overlay
            tutorial.classList.add("show");

            // Dismiss handler (clicking anywhere on the overlay or on the button)
            const dismissFunc = function (e) {
                tutorial.classList.remove("show");
                localStorage.setItem("zoom_tutorial_seen", "true");
                tutorial.removeEventListener("click", dismissFunc);
            };
            tutorial.addEventListener("click", dismissFunc);
        }
    }

    function getBounds() {
        if (!imgElement || !zoomTarget) return { minX: 0, maxX: 0, minY: 0, maxY: 0 };
        
        const containerRect = zoomTarget.getBoundingClientRect();
        const imgRect = imgElement.getBoundingClientRect();

        // Natural dimensions of the image inside the viewport
        const w = imgRect.width / scale;
        const h = imgRect.height / scale;

        const scaledW = w * scale;
        const scaledH = h * scale;

        let minX = 0, maxX = 0;
        if (scaledW > containerRect.width) {
            maxX = (scaledW - containerRect.width) / 2;
            minX = -maxX;
        }

        let minY = 0, maxY = 0;
        if (scaledH > containerRect.height) {
            maxY = (scaledH - containerRect.height) / 2;
            minY = -maxY;
        }

        return { minX, maxX, minY, maxY };
    }

    function updateTransform(animate = true) {
        if (!zoomTarget) return;
        
        // Apply boundaries
        const bounds = getBounds();
        if (scale === 1) {
            pointX = 0;
            pointY = 0;
        } else {
            pointX = Math.max(bounds.minX, Math.min(bounds.maxX, pointX));
            pointY = Math.max(bounds.minY, Math.min(bounds.maxY, pointY));
        }

        zoomTarget.style.transition = animate ? "transform 0.15s cubic-bezier(0.25, 0.46, 0.45, 0.94)" : "none";
        zoomTarget.style.transform = `translate(${pointX}px, ${pointY}px) scale(${scale})`;
    }

    // --- Mouse Event Handlers ---
    function onMouseDown(e) {
        if (e.button !== 0) return; // Only left click
        e.preventDefault();
        panning = true;
        startX = e.clientX - pointX;
        startY = e.clientY - pointY;
        zoomTarget.style.cursor = "grabbing";
    }

    function onMouseMove(e) {
        if (!panning) return;
        e.preventDefault();
        pointX = e.clientX - startX;
        pointY = e.clientY - startY;
        updateTransform(false);
    }

    function onMouseUp() {
        if (!panning) return;
        panning = false;
        if (zoomTarget) zoomTarget.style.cursor = "grab";
        updateTransform(true);
    }

    function onWheel(e) {
        e.preventDefault();
        
        const zoomFactor = 1.15;
        const oldScale = scale;

        // Mouse pivot points (zoom into cursor)
        const pivotX = e.clientX;
        const pivotY = e.clientY;

        const xs = (pivotX - pointX) / scale;
        const ys = (pivotY - pointY) / scale;

        if (e.deltaY < 0) {
            scale = Math.min(maxScale, scale * zoomFactor);
        } else {
            scale = Math.max(minScale, scale / zoomFactor);
        }

        pointX = pivotX - xs * scale;
        pointY = pivotY - ys * scale;
        updateTransform(true);
    }

    function onDoubleClick(e) {
        e.preventDefault();
        if (scale > 1) {
            scale = 1;
            pointX = 0;
            pointY = 0;
        } else {
            scale = 2.5;
            const pivotX = e.clientX;
            const pivotY = e.clientY;
            const xs = (pivotX - pointX) / 1;
            const ys = (pivotY - pointY) / 1;
            pointX = pivotX - xs * scale;
            pointY = pivotY - ys * scale;
        }
        updateTransform(true);
    }

    // --- Touch Event Handlers ---
    let touchStartDist = 0;
    let touchStartScale = 1;

    function onTouchStart(e) {
        const now = Date.now();
        const DOUBLE_TAP_DELAY = 300;

        // Double-tap zoom logic for mobile
        if (e.touches.length === 1 && (now - lastTap) < DOUBLE_TAP_DELAY) {
            e.preventDefault();
            onDoubleTap(e);
            lastTap = 0;
            return;
        }
        lastTap = now;

        if (e.touches.length === 1) {
            panning = true;
            startX = e.touches[0].clientX - pointX;
            startY = e.touches[0].clientY - pointY;
        } else if (e.touches.length === 2) {
            panning = false;
            touchStartDist = getTouchDistance(e);
            touchStartScale = scale;
        }
    }

    function onDoubleTap(e) {
        if (scale > 1) {
            scale = 1;
            pointX = 0;
            pointY = 0;
        } else {
            scale = 2.5;
            const pivotX = e.touches[0].clientX;
            const pivotY = e.touches[0].clientY;
            const xs = (pivotX - pointX) / 1;
            const ys = (pivotY - pointY) / 1;
            pointX = pivotX - xs * scale;
            pointY = pivotY - ys * scale;
        }
        updateTransform(true);
    }

    function onTouchMove(e) {
        e.preventDefault();
        if (e.touches.length === 1 && panning) {
            pointX = e.touches[0].clientX - startX;
            pointY = e.touches[0].clientY - startY;
            updateTransform(false);
        } else if (e.touches.length === 2) {
            const dist = getTouchDistance(e);
            const factor = dist / touchStartDist;
            const oldScale = scale;

            // Pinch zoom relative to midpoint of the two touches
            const midpointX = (e.touches[0].clientX + e.touches[1].clientX) / 2;
            const midpointY = (e.touches[0].clientY + e.touches[1].clientY) / 2;

            const xs = (midpointX - pointX) / scale;
            const ys = (midpointY - pointY) / scale;

            scale = Math.max(minScale, Math.min(maxScale, touchStartScale * factor));

            pointX = midpointX - xs * scale;
            pointY = midpointY - ys * scale;
            updateTransform(false);
        }
    }

    function onTouchEnd() {
        panning = false;
        updateTransform(true);
    }

    function getTouchDistance(e) {
        return Math.sqrt(
            Math.pow(e.touches[0].clientX - e.touches[1].clientX, 2) +
            Math.pow(e.touches[0].clientY - e.touches[1].clientY, 2)
        );
    }

    // --- Keyboard Navigation ---
    function onKeyDown(e) {
        if (e.key === "ArrowLeft") {
            const prevBtn = document.querySelector(".carousel-control-prev");
            if (prevBtn) prevBtn.click();
        } else if (e.key === "ArrowRight") {
            const nextBtn = document.querySelector(".carousel-control-next");
            if (nextBtn) nextBtn.click();
        } else if (e.key === "Escape") {
            const backBtn = document.querySelector(".btn-back-gallery");
            if (backBtn) backBtn.click();
        }
    }

    function destroy() {
        if (!zoomTarget) return;
        zoomTarget.removeEventListener("mousedown", onMouseDown);
        window.removeEventListener("mousemove", onMouseMove);
        window.removeEventListener("mouseup", onMouseUp);
        zoomTarget.removeEventListener("wheel", onWheel);
        zoomTarget.removeEventListener("dblclick", onDoubleClick);
        zoomTarget.removeEventListener("touchstart", onTouchStart);
        zoomTarget.removeEventListener("touchmove", onTouchMove);
        zoomTarget.removeEventListener("touchend", onTouchEnd);
        window.removeEventListener("keydown", onKeyDown);
    }

    // Expose global initializer
    window.initZoom = init;
})();
