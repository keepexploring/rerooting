"""Pelican configuration for rerooting.org.

Everything an editor is likely to want to change lives in the "Site content"
block below. Structural settings are further down and rarely need touching.
"""

import datetime

# --------------------------------------------------------------------------
# Site content
# --------------------------------------------------------------------------

AUTHOR = "Re-Rooting"
SITENAME = "Re-Rooting"
SITESUBTITLE = "Pilgrimage · Community · Creation"
SITEDESCRIPTION = (
    "Join us as we tour the UK and overseas with screenings of a new "
    "independent documentary, exploring pilgrimage, community and creation."
)
SITEURL = ""  # overridden in publishconf.py for production builds

# Hero. HERO_HEADING is rendered as-is; wrap any words you want set in the
# green italic in *asterisks*, e.g. "A deeper *belonging.*"
HERO_EYEBROW = "An independent documentary · Holy Island to Orkney by bike"
HERO_HEADING = "Faith. Place. A deeper *belonging.*"
HERO_BODY = SITEDESCRIPTION
HERO_IMAGE = "images/hero.jpg"
HERO_IMAGE_SMALL = "images/hero-1200.jpg"
HERO_IMAGE_ALT = "A road winding through a steep Highland glen under heavy cloud"

# Social sharing card. Must be 1200x630 — those dimensions are declared in the
# page head, and WhatsApp will not render a preview if they disagree.
OG_IMAGE = "images/og.jpg"
OG_IMAGE_ALT = "A road winding through a steep Highland glen under heavy cloud"

# The "the film is a beginning" section. Prose lives in content/pages/the-film.md.
ABOUT_EYEBROW = "The question behind the film"
ABOUT_HEADING = "What does the Christian faith have to do with *how we live in the natural world?*"

TRAILER_EYEBROW = "Two minutes of the road"
TRAILER_HEADING = "Watch the trailer."
TRAILER_POSTER = "images/trailer-poster.jpg"

ABOUT_IMAGE = "images/community.jpg"
ABOUT_IMAGE_ALT = "A woman and a dog walking two ponies down a croft track, houses and hills behind"

SCREENINGS_EYEBROW = "Where to see it"
SCREENINGS_HEADING = "Screenings & *gatherings.*"
SCREENINGS_EMPTY = (
    "Nothing in the diary at the moment. Get in touch and we’ll tell you when "
    "the next one is booked."
)

# The enquiry form on the Contact page. Web3Forms emails each message to the
# address the key was created for; nothing is stored on their side. Get a key
# at https://web3forms.com — it is meant to live in public HTML.
WEB3FORMS_KEY = "4eba7c12-720c-4fd9-a4ee-e86ba1d01979"

# Where people land after sending. Must be a page that exists in content/pages.
ENQUIRY_SUCCESS_URL = "message-sent/"

# hCaptcha on the contact form. This must match the Captcha Protection setting
# in the Web3Forms dashboard: if it is set to hCaptcha there and False here,
# every submission is rejected.
#
# Note this is the one place the site loads third-party JavaScript, and the
# form stops working for anyone with JavaScript off. Set to False if the
# Advanced Spam Filter proves enough on its own.
HCAPTCHA_ENABLED = True

ENQUIRY_HEADING = "Send us *a message.*"
ENQUIRY_BODY = (
    "Tell us where you are, who you have in mind and roughly when, and we’ll "
    "take it from there."
)


# Gallery. Stills from the ride, taken from the slide deck. Each entry is
# (filename under content/images/gallery/, alt text). The homepage shows the
# first GALLERY_HOME_COUNT of these; the film page shows them all.
GALLERY_EYEBROW = "A thousand miles"
GALLERY_HEADING = "Pictures from *the road.*"
GALLERY_HOME_COUNT = 6
GALLERY = [
    ("causeway-sands", "A lone rider on the causeway, with tidal sands stretching away on either side"),
    ("glen-climb", "Two loaded bikes on a stony path winding up a Highland glen"),
    ("croft-ruins", "Looking straight down on two roofless stone croft houses, the riders inside"),
    ("lochan-road", "A single-track road threading between lochans across open moor"),
    ("beach-camp", "Two tents pitched above a beach at dusk, surf breaking beyond"),
    ("forest-track", "Two riders on a track through dense forestry"),
    ("loch-and-sheep", "Riding a road beside a sea loch, a line of sheep on the shore"),
    ("dusk-castle", "Riding into the dusk past a castle, a red rear light on the road"),
    ("pitching-camp", "Pitching a tent on the grass in the last of the light"),
    ("track-from-above", "A track seen from directly above, cutting between moss and forestry"),
]

# Production credit, given its own band above the footer on every page.
CREDIT_EYEBROW = "An independent film by"
FILM_BY = ("Wildris Media", "https://www.wildrismedia.com")
FILM_PARTNER = ("CREATIVenergie", "https://creativenergie.co.uk")

# Drop logo files into content/images/ and name them here to use artwork in
# place of the names above. SVG or a transparent PNG works best, since the
# band is cream rather than white. Leave empty to show the names as type.
FILM_BY_LOGO = ""
FILM_PARTNER_LOGO = ""

# Footer photo credits. Replace once all imagery comes from the film.
PHOTO_CREDITS = [
    ("Stills from Re-Rooting", None),
]

SOCIAL = [
    ("YouTube", "https://www.youtube.com/watch?v=q0MAijKW7ZQ"),
]

# Set to True once a podcast exists; this reveals the Podcast nav item.
PODCAST_ENABLED = False

# --------------------------------------------------------------------------
# Structure
# --------------------------------------------------------------------------

PATH = "content"
OUTPUT_PATH = "output"
THEME = "theme/rerooting"

# Header navigation. (label, path) — path is relative to the site root,
# with no leading slash, so it keeps working in local relative-URL builds.
# The button at the right of the header. (label, path) — while the mailing
# list is parked this points at the contact page rather than the signup.
NAV_CTA = ("Continue the conversation", "contact/")

MENUITEMS = [
    ("The film", "the-film/"),
    ("Screenings", "#screenings"),
    ("Contact", "contact/"),
]
DISPLAY_PAGES_ON_MENU = False
DISPLAY_CATEGORIES_ON_MENU = False

TIMEZONE = "Europe/London"
DEFAULT_LANG = "en"
DEFAULT_DATE_FORMAT = "%-d %B %Y"

# Screenings are articles; everything else is a page.
ARTICLE_PATHS = ["screenings"]
ARTICLE_URL = "screenings/{slug}/"
ARTICLE_SAVE_AS = "screenings/{slug}/index.html"
ARTICLE_ORDER_BY = "date"

PAGE_PATHS = ["pages"]
PAGE_URL = "{slug}/"
PAGE_SAVE_AS = "{slug}/index.html"
PAGE_ORDER_BY = "sortorder"

STATIC_PATHS = ["images", "extra"]
EXTRA_PATH_METADATA = {
    "extra/CNAME": {"path": "CNAME"},
    "extra/robots.txt": {"path": "robots.txt"},
}

# A landing-page site: no tag clouds, author pages or date archives.
DIRECT_TEMPLATES = ["index"]
INDEX_SAVE_AS = "index.html"
CATEGORY_SAVE_AS = ""
CATEGORY_URL = ""
TAG_SAVE_AS = ""
AUTHOR_SAVE_AS = ""
AUTHORS_SAVE_AS = ""
CATEGORIES_SAVE_AS = ""
TAGS_SAVE_AS = ""
ARCHIVES_SAVE_AS = ""
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

RELATIVE_URLS = True
DELETE_OUTPUT_DIRECTORY = True
CACHE_CONTENT = False
LOAD_CONTENT_CACHE = False

MARKDOWN = {
    "extension_configs": {
        "markdown.extensions.extra": {},
        "markdown.extensions.meta": {},
        "markdown.extensions.smarty": {},
    },
    "output_format": "html5",
}


# --------------------------------------------------------------------------
# Template helpers
# --------------------------------------------------------------------------


def _now():
    """Build-time 'now', timezone-aware so it can be compared to article dates.

    Whether a screening counts as upcoming is therefore decided when the site
    is built, not when it is viewed. The deploy workflow runs on a daily cron
    so that past screenings drop off the homepage without anyone pushing.
    """
    try:
        from zoneinfo import ZoneInfo

        return datetime.datetime.now(ZoneInfo(TIMEZONE))
    except Exception:  # pragma: no cover - fallback for odd environments
        return datetime.datetime.now()


def _aware(value, reference):
    """Make `value` comparable with `reference` (both aware or both naive)."""
    if reference.tzinfo is None and value.tzinfo is not None:
        return value.replace(tzinfo=None)
    if reference.tzinfo is not None and value.tzinfo is None:
        return value.replace(tzinfo=reference.tzinfo)
    return value


def upcoming(articles):
    """Screenings still to come, soonest first."""
    now = _now()
    items = [a for a in articles if _aware(a.date, now) >= now]
    return sorted(items, key=lambda a: a.date)


def past(articles):
    """Screenings that have already happened, most recent first."""
    now = _now()
    items = [a for a in articles if _aware(a.date, now) < now]
    return sorted(items, key=lambda a: a.date, reverse=True)


def accent(text):
    """Render *starred* words in the display serif italic accent colour.

    Lets headings be written as plain strings in this file, e.g.
    "A deeper *belonging.*" -> "A deeper <em class='accent'>belonging.</em>"
    """
    import html
    import re

    from markupsafe import Markup

    parts = re.split(r"\*(.+?)\*", str(text))
    out = []
    for index, part in enumerate(parts):
        escaped = html.escape(part)
        out.append(f'<em class="accent">{escaped}</em>' if index % 2 else escaped)
    return Markup("".join(out))


def intro(html_content):
    """A page's HTML up to its first `##` heading.

    The homepage shows the opening of content/pages/the-film.md this way, so
    everything above the first `##` in that file is also the homepage intro.
    """
    from markupsafe import Markup

    text = str(html_content)
    cut = text.find("<h2")
    return Markup(text if cut == -1 else text[:cut])


JINJA_FILTERS = {
    "upcoming": upcoming,
    "past": past,
    "accent": accent,
    "intro": intro,
}

JINJA_GLOBALS = {
    "build_year": _now().year,
}
