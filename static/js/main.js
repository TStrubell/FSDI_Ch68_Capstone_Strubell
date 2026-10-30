"use strict";

/* =========================================================
   CINEMATIC SGnG MARKETPLACE
   Global JavaScript
   ========================================================= */


/* =========================================================
   DOCUMENT STATE
   ========================================================= */

document.documentElement.classList.add("js");


/* =========================================================
   DOM READY
   ========================================================= */

document.addEventListener("DOMContentLoaded", () => {
    initializeExternalLinks();
    initializeMarketplaceFilters();
    initializeKeyboardHelpers();
});


/* =========================================================
   EXTERNAL LINKS
   ========================================================= */

function initializeExternalLinks() {
    const externalLinks = document.querySelectorAll(
        'a[target="_blank"]'
    );

    externalLinks.forEach((link) => {
        const existingRel =
            link.getAttribute("rel") || "";

        const relValues =
            new Set(existingRel.split(/\s+/).filter(Boolean));

        relValues.add("noopener");
        relValues.add("noreferrer");

        link.setAttribute(
            "rel",
            Array.from(relValues).join(" ")
        );
    });
}


/* =========================================================
   MARKETPLACE FILTER ENHANCEMENTS
   ========================================================= */

function initializeMarketplaceFilters() {
    const filterForm =
        document.querySelector(".marketplace-filters");

    if (!filterForm) {
        return;
    }

    const searchInput =
        filterForm.querySelector(
            'input[name="q"]'
        );

    const selects =
        filterForm.querySelectorAll("select");

    selects.forEach((select) => {
        select.addEventListener("change", () => {
            select.classList.toggle(
                "has-value",
                Boolean(select.value)
            );
        });

        select.classList.toggle(
            "has-value",
            Boolean(select.value)
        );
    });

    if (searchInput) {
        searchInput.addEventListener(
            "keydown",
            (event) => {
                if (event.key === "Escape") {
                    searchInput.value = "";
                }
            }
        );
    }
}


/* =========================================================
   KEYBOARD HELPERS
   ========================================================= */

function initializeKeyboardHelpers() {
    document.addEventListener(
        "keydown",
        (event) => {
            if (event.key !== "Escape") {
                return;
            }

            const activeElement =
                document.activeElement;

            if (
                activeElement instanceof
                HTMLInputElement
            ) {
                activeElement.blur();
            }
        }
    );
}