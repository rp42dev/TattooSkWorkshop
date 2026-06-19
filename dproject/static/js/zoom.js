(function () {
    let scale = 1;
    let pointX = 0;
    let pointY = 0;
    let startX = 0;
    let startY = 0;
    let panning = false;
    let prevDistance = 0;
    let zoomTarget = null;
    let lastTap = 0;

    const maxScale = 4.0;
    const minScale = 1.0;

    function init() {
        // Clean up previous instance if it exists to prevent listener leaks on HTMX swaps
        if (typeof window.destroyZoom === "function") {
            window.destroyZoom();
        }

        // Target the actual image container (.item-gallery) instead of the full screen container
        zoomTarget = document.querySelector(".item-gallery");
        if (!zoomTarget) return;

        // Reset positions
        scale = 1;
        pointX = 0;
        pointY = 0;
        updateTransform(false);

        // Remove any old event listeners (clean state)
        destroy();

        // PC Listeners
        zoomTarget.addEventListener("mousedown", onMouseDown);
        zoomTarget.addEventListener("dragstart", onDragStart);
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

        // Register current destroy function globally for HTMX/SPAs clean cleanup
        window.destroyZoom = destroy;
    }

    function initTutorial() {
        const tutorial = document.querySelector("#zoom-tutorial");
        if (!tutorial) return;

        // Dismiss handler (clicking anywhere on the overlay or on the button)
        const dismissFunc = function (e) {
            tutorial.classList.remove("show");
            localStorage.setItem("zoom_tutorial_seen", "true");
        };
        tutorial.removeEventListener("click", dismissFunc);
        tutorial.addEventListener("click", dismissFunc);

        const tutorialSeen = localStorage.getItem("zoom_tutorial_seen");
        if (!tutorialSeen) {
            tutorial.classList.add("show");
        }

        // Handle reopen button
        const reopenBtn = document.querySelector("#reopen-tutorial-btn");
        if (reopenBtn) {
            reopenBtn.onclick = function (e) {
                e.stopPropagation();
                tutorial.classList.add("show");
            };
        }
    }

    function getBounds() {
        if (!zoomTarget || !zoomTarget.parentElement) return { minX: 0, maxX: 0, minY: 0, maxY: 0 };
        
        const viewportW = zoomTarget.parentElement.clientWidth;
        const viewportH = zoomTarget.parentElement.clientHeight;
        
        const scaledW = zoomTarget.offsetWidth * scale;
        const scaledH = zoomTarget.offsetHeight * scale;

        let minX = 0, maxX = 0;
        if (scaledW > viewportW) {
            maxX = (scaledW - viewportW) / 2;
            minX = -maxX;
        }

        let minY = 0, maxY = 0;
        if (scaledH > viewportH) {
            maxY = (scaledH - viewportH) / 2;
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
        zoomTarget.style.transformOrigin = "center center";
        zoomTarget.style.transform = `translate(${pointX}px, ${pointY}px) scale(${scale})`;
    }

    // --- Mouse Event Handlers ---
    function onDragStart(e) {
        e.preventDefault();
    }

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

        if (e.deltaY < 0) {
            scale = Math.min(maxScale, scale * zoomFactor);
        } else {
            scale = Math.max(minScale, scale / zoomFactor);
        }

        if (scale !== oldScale) {
            const viewport = zoomTarget.parentElement.getBoundingClientRect();
            const viewportCenterX = viewport.left + viewport.width / 2;
            const viewportCenterY = viewport.top + viewport.height / 2;

            // Mouse offset from viewport center
            const dx = e.clientX - viewportCenterX;
            const dy = e.clientY - viewportCenterY;

            // Zoom relative to mouse cursor position
            pointX = dx * (1 - scale);
            pointY = dy * (1 - scale);
            updateTransform(true);
        }
    }

    function onDoubleClick(e) {
        e.preventDefault();
        if (scale > 1) {
            scale = 1;
            pointX = 0;
            pointY = 0;
        } else {
            scale = 2.5;
            const viewport = zoomTarget.parentElement.getBoundingClientRect();
            const viewportCenterX = viewport.left + viewport.width / 2;
            const viewportCenterY = viewport.top + viewport.height / 2;

            const dx = e.clientX - viewportCenterX;
            const dy = e.clientY - viewportCenterY;

            pointX = dx * (1 - scale);
            pointY = dy * (1 - scale);
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
            const viewport = zoomTarget.parentElement.getBoundingClientRect();
            const viewportCenterX = viewport.left + viewport.width / 2;
            const viewportCenterY = viewport.top + viewport.height / 2;

            const dx = e.touches[0].clientX - viewportCenterX;
            const dy = e.touches[0].clientY - viewportCenterY;

            pointX = dx * (1 - scale);
            pointY = dy * (1 - scale);
        }
        updateTransform(true);
    }

    function onTouchMove(e) {
        e.preventDefault();
        if (e.touches.length === 1) {
            if (!panning) {
                panning = true;
                startX = e.touches[0].clientX - pointX;
                startY = e.touches[0].clientY - pointY;
            }
            pointX = e.touches[0].clientX - startX;
            pointY = e.touches[0].clientY - startY;
            updateTransform(false);
        } else if (e.touches.length === 2) {
            const dist = getTouchDistance(e);
            const factor = dist / touchStartDist;
            const oldScale = scale;

            // Midpoint of the two fingers
            const midpointX = (e.touches[0].clientX + e.touches[1].clientX) / 2;
            const midpointY = (e.touches[0].clientY + e.touches[1].clientY) / 2;

            const viewport = zoomTarget.parentElement.getBoundingClientRect();
            const viewportCenterX = viewport.left + viewport.width / 2;
            const viewportCenterY = viewport.top + viewport.height / 2;

            const dx = midpointX - viewportCenterX;
            const dy = midpointY - viewportCenterY;

            scale = Math.max(minScale, Math.min(maxScale, touchStartScale * factor));

            pointX = dx * (1 - scale);
            pointY = dy * (1 - scale);
            updateTransform(false);
        }
    }

    // Fixed: Touchend should clean up and pan back within boundaries properly
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
        if (zoomTarget) {
            zoomTarget.removeEventListener("mousedown", onMouseDown);
            zoomTarget.removeEventListener("dragstart", onDragStart);
            zoomTarget.removeEventListener("wheel", onWheel);
            zoomTarget.removeEventListener("dblclick", onDoubleClick);
            zoomTarget.removeEventListener("touchstart", onTouchStart);
            zoomTarget.removeEventListener("touchmove", onTouchMove);
            zoomTarget.removeEventListener("touchend", onTouchEnd);
        }
        window.removeEventListener("mousemove", onMouseMove);
        window.removeEventListener("mouseup", onMouseUp);
        window.removeEventListener("keydown", onKeyDown);
    }

    // Expose global initializer
    window.initZoom = init;
})();
