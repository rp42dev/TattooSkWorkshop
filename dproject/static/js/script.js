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

});