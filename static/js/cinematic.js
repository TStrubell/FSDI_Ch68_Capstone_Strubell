"use strict";

/* =========================================================
   CINEMATIC SGnG MARKETPLACE
   Cinematic Progressive Enhancement
   ========================================================= */


document.addEventListener("DOMContentLoaded", () => {
    initializeCinematicExperience();
});


/* =========================================================
   INITIALIZATION
   ========================================================= */

function initializeCinematicExperience() {
    const revealElements =
        document.querySelectorAll(
            ".cinematic-reveal"
        );

    if (!revealElements.length) {
        return;
    }

    const prefersReducedMotion =
        window.matchMedia(
            "(prefers-reduced-motion: reduce)"
        ).matches;

    if (prefersReducedMotion) {
        revealAll(revealElements);
        return;
    }

    const hasGsap =
        typeof window.gsap !== "undefined";

    const hasScrollTrigger =
        typeof window.ScrollTrigger !==
        "undefined";

    if (hasGsap && hasScrollTrigger) {
        initializeGsapAnimations(
            revealElements
        );

        return;
    }

    initializeNativeReveal(
        revealElements
    );
}


/* =========================================================
   GSAP VERSION
   ========================================================= */

function initializeGsapAnimations(
    revealElements
) {
    const gsap = window.gsap;
    const ScrollTrigger =
        window.ScrollTrigger;

    gsap.registerPlugin(ScrollTrigger);

    revealElements.forEach(
        (element) => {
            gsap.fromTo(
                element,
                {
                    opacity: 0,
                    y: 32,
                },
                {
                    opacity: 1,
                    y: 0,
                    duration: 0.8,
                    ease: "power2.out",

                    scrollTrigger: {
                        trigger: element,
                        start: "top 88%",
                        once: true,
                    },
                }
            );
        }
    );

    const heroTitle =
        document.querySelector(
            ".home-hero__title"
        );

    const heroSummary =
        document.querySelector(
            ".home-hero__summary"
        );

    const heroActions =
        document.querySelector(
            ".home-hero__actions"
        );

    const heroElements = [
        heroTitle,
        heroSummary,
        heroActions,
    ].filter(Boolean);

    if (heroElements.length) {
        gsap.fromTo(
            heroElements,
            {
                opacity: 0,
                y: 28,
            },
            {
                opacity: 1,
                y: 0,
                duration: 0.9,
                stagger: 0.12,
                ease: "power2.out",
            }
        );
    }
}


/* =========================================================
   NATIVE BROWSER FALLBACK
   ========================================================= */

function initializeNativeReveal(
    revealElements
) {
    if (
        !(
            "IntersectionObserver"
            in window
        )
    ) {
        revealAll(revealElements);
        return;
    }

    const observer =
        new IntersectionObserver(
            (entries) => {
                entries.forEach(
                    (entry) => {
                        if (
                            !entry.isIntersecting
                        ) {
                            return;
                        }

                        entry.target.style.opacity =
                            "1";

                        entry.target.style.transform =
                            "translateY(0)";

                        entry.target.style.transition =
                            [
                                "opacity 700ms ease",
                                "transform 700ms ease",
                            ].join(", ");

                        observer.unobserve(
                            entry.target
                        );
                    }
                );
            },
            {
                threshold: 0.15,
                rootMargin:
                    "0px 0px -5% 0px",
            }
        );

    revealElements.forEach(
        (element) => {
            observer.observe(element);
        }
    );
}


/* =========================================================
   ACCESSIBILITY FALLBACK
   ========================================================= */

function revealAll(elements) {
    elements.forEach((element) => {
        element.style.opacity = "1";
        element.style.transform = "none";
    });
}