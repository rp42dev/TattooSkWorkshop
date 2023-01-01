
// // Lazy load images
// $(window).on("load", function () {
//     $(window).scroll(function () {
//         var windowBottom = $(this).scrollTop() + $(this).innerHeight();
//         $(".fade").each(function () {
//             var objectBottom = $(this).offset().top + 50;
//             if (objectBottom < windowBottom) {
//                 $(this).removeClass('fade');
//             }
//         });
//     }).scroll();
// });


function initFade() {
    gsap.registerPlugin(ScrollTrigger);

    gsap.utils.toArray(["article"]).forEach((panel) => {
        panel.classList.add("fade");
    });

    gsap.utils.toArray(".fade").forEach((panel) => {
        gsap.timeline({
            scrollTrigger: {
                trigger: panel,
                start: "top bottom",
                end: "bottom",
                scrub: 2,
                // markers: true,
            },
        })
            .fromTo(panel, {
                opacity: 0,
                y: panel.offsetHeight / 10
            }, {
                opacity: 1,
                y: 0
            })
    });
}

$(window).on("load", function () {

    gsap.registerPlugin(ScrollTrigger);
    
    gsap.fromTo(".masthead-content h1", {
        opacity: 0,
        scale: 0.9,
    }, {
        opacity: 0.8,
        scale: 1,
        duration: 0.5,
        ease: "back.out(1.7)",
    });
    
    gsap.fromTo(".slogan h2", {
        opacity: 0,
        scale: 0.9,
    }, {
        delay: 0.2,
        opacity: 0.8,
        scale: 1,
        duration: 0.5,
        ease: "back.out(1.7)",
    });

    initFade();
});
