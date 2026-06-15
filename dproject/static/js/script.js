document.body.addEventListener('htmx:afterSwap', function (event) {

    var lazyImages = [].slice.call(document.querySelectorAll("img.lazy"));
    if ("IntersectionObserver" in window) {
        let lazyImageObserver = new IntersectionObserver(function (entries, observer) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    let lazyImage = entry.target;
                    lazyImage.src = lazyImage.dataset.src;
                    lazyImage.srcset = lazyImage.dataset.srcset;
                    lazyImage.classList.remove("lazy");
                    lazyImageObserver.unobserve(lazyImage);
                }
            });
        });
        lazyImages.forEach(function (lazyImage) {
            lazyImageObserver.observe(lazyImage);
        });
    } else {
        // Possibly fall back to a more compatible method here

    }

    var articles = [].slice.call(document.querySelectorAll("article"));
    var sectionHeaders = document.querySelectorAll(".section-header");
    
    sectionHeaders.forEach(function (sectionHeader) {
        sectionHeader.classList.add("lazy-element");
    });

    articles.forEach(function (article) {
        article.classList.add("lazy-element");
    });

    var lazyElement = [].slice.call(document.querySelectorAll(".lazy-element"));
    if ("IntersectionObserver" in window) {
        let lazyElementObserver = new IntersectionObserver(function (entries, observer) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    let lazyElement = entry.target;
                    lazyElement.classList.add("lazy-element--visible");
                    lazyElementObserver.unobserve(lazyElement);
                }
            });
        });
        lazyElement.forEach(function (lazyElement) {
            lazyElementObserver.observe(lazyElement);
        });
    } else {
        // Possibly fall back to a more compatible method here

    }

    // Initialize Carousels for HTMX loaded content
    var carousels = document.querySelectorAll('.carousel');
    carousels.forEach(function (carousel) {
        if (typeof bootstrap !== 'undefined') {
            new bootstrap.Carousel(carousel);
        }
    });

});

// ── Parallax Banners – Entrance Observer ─────────────────────────────────────
document.addEventListener('DOMContentLoaded', function () {
    var banners = document.querySelectorAll('.parallax-section-banner');
    if (!banners.length) return;

    if ('IntersectionObserver' in window) {
        var bannerObserver = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    entry.target.classList.add('in-view');
                    bannerObserver.unobserve(entry.target);
                }
            });
        }, { threshold: 0.15 });

        banners.forEach(function (b) { bannerObserver.observe(b); });
    } else {
        banners.forEach(function (b) { b.classList.add('in-view'); });
    }
});

document.addEventListener('DOMContentLoaded', function () {
    var hamburger = document.querySelector('.premium-hamburger');
    var menuEl    = document.getElementById('menu');

    if (!hamburger || !menuEl) return;

    menuEl.addEventListener('show.bs.offcanvas', function () {
        hamburger.classList.add('is-active');
    });
    menuEl.addEventListener('hide.bs.offcanvas', function () {
        hamburger.classList.remove('is-active');
    });
});