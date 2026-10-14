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

  /* ------------------------------------------------ email addresses --- */
  /* The address is never written into the HTML as one string: the page ships
     the local part and the domain in separate attributes, and they are only
     joined together here, in the browser, when someone asks for it. Harvesters
     that scrape the raw HTML (most of them) find nothing to take. Without
     JavaScript the <noscript> fallback inside the span still tells a human how
     to reach us. */
  var slots = document.querySelectorAll("[data-email-user][data-email-domain]");

  Array.prototype.forEach.call(slots, function (slot) {
    var address =
      slot.getAttribute("data-email-user") +
      String.fromCharCode(64) +
      slot.getAttribute("data-email-domain");

    var button = document.createElement("button");
    button.type = "button";
    button.className = "email-reveal";
    button.textContent = slot.getAttribute("data-email-label") || "Show email address";

    button.addEventListener("click", function () {
      var link = document.createElement("a");
      link.href = "mailto:" + address;
      link.className = "email-address";
      link.textContent = address;
      slot.replaceChildren(link);
      link.focus();
    });

    slot.replaceChildren(button);
  });

  /* ------------------------------------------------- signup niceties -- */
  /* Brevo handles the real validation server-side; this just gives people
     an immediate, readable message instead of only the browser default. */
  var form = document.querySelector(".signup__form");

  if (form && !form.hasAttribute("data-unconfigured")) {
    form.addEventListener("submit", function (event) {
      var consent = form.querySelector('input[name="OPT_IN"]');
      var existing = form.querySelector(".form-error");

      if (existing) existing.remove();

      if (consent && !consent.checked) {
        event.preventDefault();
        var message = document.createElement("p");
        message.className = "form-error";
        message.setAttribute("role", "alert");
        message.textContent =
          "Please tick the box to confirm you'd like to hear from us.";
        consent.insertAdjacentElement("afterend", message);
        consent.focus();
      }
    });
  }
})();
