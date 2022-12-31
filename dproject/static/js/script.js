
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

$(window).on("load", function () {


    gsap.registerPlugin(ScrollTrigger);

    setTimeout(() => {
        gsap.fromTo(".slogan h2", {
            opacity: 0,
            y: 100,
            scale: 0.9,
        }, {
            opacity: 0.8,
            y: 0,
            scale: 1,
            duration: 0.5,
            ease: "back.out(1.7)",
        });

        gsap.utils.toArray(["article"]).forEach((panel) => {
            panel.classList.add("fade");
        });

        gsap.fromTo(".masthead-content h1", {
            opacity: 0,
            y: 100,
            scale: 0.9,
        }, {
            opacity: 0.8,
            y: 0,
            scale: 1,
            duration: 0.5,
            ease: "back.out(1.7)",
        });

        gsap.utils.toArray(".fade").forEach((panel) => {
            const tl = gsap.timeline({
                scrollTrigger: {
                    trigger: panel,
                    start: "top bottom",
                    end: "+=50%",
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

        gsap.utils.toArray(".img").forEach((panel) => {
            let sctubData = panel.getAttribute("data-scroll-scrub");
            const tl = gsap.timeline({
                scrollTrigger: {
                    trigger: panel,
                    start: "top bottom",
                    end: "+=90%",
                    scrub: (sctubData == null) ? 1 : sctubData,
                    // markers: true,
                },
            })
                .fromTo(panel, {
                    scale: 1.1,
                }, {
                    duration: 0.8,
                    scale: 1,
                    ease: "back.out(1.7)"
                })
                .fromTo(panel, {
                    filter: 'grayscale(0.8) blur(2px)',
                }, {
                    filter: 'grayscale(0) blur(0px)',
                    duration: 0.3,
                    delay: 0.3,
                }, 0)

        });



    }, 100);

});
