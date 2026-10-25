"use strict";

const navigationToggle =
    document.querySelector(".nav-toggle");

const primaryNavigation =
    document.querySelector(".primary-navigation");

if (navigationToggle && primaryNavigation) {
    navigationToggle.addEventListener(
        "click",
        () => {
            const isOpen =
                primaryNavigation.classList.toggle(
                    "is-open"
                );

            navigationToggle.setAttribute(
                "aria-expanded",
                String(isOpen)
            );
        }
    );

    primaryNavigation.addEventListener(
        "click",
        (event) => {
            const clickedLink =
                event.target.closest("a");

            if (!clickedLink) {
                return;
            }

            primaryNavigation.classList.remove(
                "is-open"
            );

            navigationToggle.setAttribute(
                "aria-expanded",
                "false"
            );
        }
    );

    document.addEventListener(
        "keydown",
        (event) => {
            if (event.key !== "Escape") {
                return;
            }

            primaryNavigation.classList.remove(
                "is-open"
            );

            navigationToggle.setAttribute(
                "aria-expanded",
                "false"
            );

            navigationToggle.focus();
        }
    );
}
