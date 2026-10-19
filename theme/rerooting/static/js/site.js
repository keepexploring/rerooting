/* Re-Rooting — the small amount of behaviour the site needs.
   No dependencies; everything degrades to working HTML without it. */
(function () {
  "use strict";

  /* ---------------------------------------------------- mobile nav ---- */
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.getElementById("site-nav");

  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", String(open));
    });
  }

  /* ------------------------------------------------ trailer facade ---- */
  /* Nothing is requested from YouTube until someone presses play. That
     keeps the page quick and avoids third-party cookies on first visit. */
  var facade = document.querySelector(".trailer__facade");

  if (facade) {
    facade.addEventListener("click", function () {
      var id = facade.getAttribute("data-youtube-id");
      if (!id) return;

      var iframe = document.createElement("iframe");
      iframe.src =
        "https://www.youtube-nocookie.com/embed/" +
        encodeURIComponent(id) +
        "?autoplay=1&rel=0&modestbranding=1";
      iframe.title = facade.getAttribute("data-title") || "Trailer";
      iframe.allow =
        "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture";
      iframe.allowFullscreen = true;

      facade.replaceWith(iframe);
      iframe.focus();
    });
  }

  /* ------------------------------------------------- enquiry captcha -- */
  /* Web3Forms rejects a submission with no captcha token, and the rejection
     is a bare JSON error page. Catch it here instead and say so in place. */
  var enquiry = document.querySelector(".enquiry__form");

  if (enquiry && enquiry.querySelector(".h-captcha")) {
    enquiry.addEventListener("submit", function (event) {
      var token = enquiry.querySelector('textarea[name="h-captcha-response"]');
      var existing = enquiry.querySelector(".form-error");

      if (existing) existing.remove();

      if (!token || !token.value) {
        event.preventDefault();
        var message = document.createElement("p");
        message.className = "form-error";
        message.setAttribute("role", "alert");
        message.textContent =
          "Please tick the box below to show you're not a robot.";
        enquiry.querySelector(".h-captcha").insertAdjacentElement("afterend", message);
      }
    });
  }

})();
