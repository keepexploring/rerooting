# rerooting.org

The website for **Re-Rooting**, a documentary about a thousand-mile cycle
pilgrimage from Holy Island to Orkney.

Built with [Pelican](https://getpelican.com) (Python). Content is Markdown, so
most day-to-day edits can be made in the GitHub web editor without running
anything locally. Pushing to `main` deploys automatically.

---

## Running it locally

You need Python 3.9+.

```bash
make install   # creates .venv and installs dependencies
make serve     # http://localhost:8000, rebuilds as you edit
```

The project can live in any folder, and can be moved after setup — `.venv`
can't be relocated, so the Makefile notices when it has gone stale and
rebuilds it on the next command.

Other targets:

| Command | What it does |
| --- | --- |
| `make html` | One-off build into `output/` |
| `make publish` | Production build (absolute URLs) — what CI runs |
| `make frames` | Re-extract still images from the trailer |
| `make clean` | Delete `output/` |

---

## The three things you'll actually edit

### 1. Adding a screening

Create a file in `content/screenings/`, named `YYYY-MM-DD-where.md`:

```markdown
Title: An evening of film & conversation
Date: 2026-11-14 19:30
Slug: glasgow-november-2026
City: Glasgow
Venue: Wellington Church
Address: 77 Southpark Avenue, Glasgow G12 8LE
Eventbrite: https://www.eventbrite.co.uk/e/your-real-event-id
Cta: Reserve your seat
Standfirst: One line that appears under the title.

The body text, in Markdown. This shows on the screening's own page.
```

That's all that's needed. The site then:

- puts the **soonest upcoming** screening in the sage bar under the hero,
- lists all upcoming screenings in the Screenings section,
- gives the screening its own page at `/screenings/<slug>/`,
- moves it into the collapsed "Past screenings" list once the date has passed.

`Eventbrite`, `Cta`, `Standfirst` and `Address` are all optional. Without an
Eventbrite link the card links to the screening's own page instead.

> **Note:** past/upcoming is decided when the site is *built*. A GitHub Actions
> cron rebuilds every night at 04:17 UTC so finished events drop off by
> themselves.

### 2. Editing page text

- `content/pages/the-film.md` — the "The film" page. Everything **above the
  first `##` heading** is also used as the homepage intro, so keep the opening
  paragraphs self-contained.
- `content/pages/contact.md` — the Contact page.
- `content/pages/thank-you.md` — where Brevo sends people after they sign up.

### 3. Headings, labels and settings

The short strings — hero headline, section eyebrows, the mailing-list copy —
live at the top of `pelicanconf.py` under "Site content". Each is commented.

Wrap words in `*asterisks*` to set them in the green serif italic:

```python
HERO_HEADING = "Faith. Place. A deeper *belonging.*"
```

---

## Connecting the mailing list (Brevo)

The signup form is plain HTML that posts directly to Brevo, so there is no
backend to run or maintain. Until it's connected, the form renders disabled
with a visible "not connected yet" notice — it never silently drops addresses.

1. In Brevo, go to **Contacts → Forms** and create a form.
2. Add an **EMAIL** field, and a checkbox field named **OPT_IN** for the
   consent tick-box. (If you'd rather not record consent as an attribute,
   delete the `OPT_IN` input from `theme/rerooting/templates/partials/signup.html`.)
3. Under **Share**, choose the **Simple HTML** option — the one that doesn't
   need JavaScript.
4. Copy the URL out of its `<form action="...">`. It looks like
   `https://1a2b3c4d.sibforms.com/serve/MUIFA...`
5. Paste it into `pelicanconf.py`:

   ```python
   BREVO_FORM_ACTION = "https://1a2b3c4d.sibforms.com/serve/MUIFA..."
   ```

6. In Brevo's form settings, set the confirmation redirect to
   `https://rerooting.org/thank-you/`.

Turn on double opt-in in Brevo. It keeps the list clean and keeps you on the
right side of UK GDPR.

---

## Deploying

`.github/workflows/deploy.yml` builds the site and publishes it to GitHub
Pages on every push to `main`.

**One-time setup:**

1. In the repository, go to **Settings → Pages** and set **Source** to
   **GitHub Actions**.
2. Point the domain at GitHub. At your DNS provider, for `rerooting.org`:

   | Type | Name | Value |
   | --- | --- | --- |
   | A | `@` | `185.199.108.153` |
   | A | `@` | `185.199.109.153` |
   | A | `@` | `185.199.110.153` |
   | A | `@` | `185.199.111.153` |
   | CNAME | `www` | `<your-github-username>.github.io.` |

3. Back in **Settings → Pages**, enter `rerooting.org` as the custom domain and
   tick **Enforce HTTPS** once the certificate has been issued.

`content/extra/CNAME` already contains `rerooting.org` and is copied into the
build, so the custom domain survives each deploy.

---

## Imagery

All stills currently come from the trailer. `scripts/extract-frames.sh` handles
this, using `yt-dlp` and `ffmpeg` installed from `requirements-dev.txt` — no
Homebrew needed. `make frames` installs them for you; to run the script
directly first do `make install-dev`.

```bash
./scripts/extract-frames.sh          # dump candidate frames + contact sheets
./scripts/extract-frames.sh preset   # rebuild the exact images the site uses
./scripts/extract-frames.sh 00:02:26 hero   # grab one specific moment
```

Candidates and contact sheets land in `scripts/.trailer/` (git-ignored). The
sheets tile one frame every 2 seconds, so the Nth tile is at `(N-1)×2` seconds.

The trailer is 1920×1080 with the 2.35:1 image letterboxed inside it; the
script crops the black bars off automatically.

The frames currently in use are listed in the `preset` block of that script.
When you have proper film stills, drop them into `content/images/` with the
same filenames and they'll be picked up — or change the paths in
`pelicanconf.py`.

---

## Adding the podcast later

The groundwork is in place; nothing needs restructuring.

1. Add `content/podcast/` and point Pelican at it as a second article source.
2. Give each episode an `Audio:` metadata field with the MP3 URL.
3. Set `PODCAST_ENABLED = True` in `pelicanconf.py` — this reveals the Podcast
   item already wired into the header navigation.
4. Generate an RSS feed with `<enclosure>` elements (Apple Podcasts and Spotify
   both need these). Pelican's built-in Atom feeds don't do enclosures, so this
   means either a small custom feed template or the
   [`pelican-podcast-feed`](https://github.com/magnunleno/pelican-podcast-feed)
   plugin.

Hosting the audio itself is the one piece this repo can't cover — GitHub Pages
has a 1 GB repository limit and isn't meant for media. A dedicated podcast host
is the usual answer.

---

## How it's put together

```
content/
  pages/        Markdown pages (the film, contact, thank-you)
  screenings/   One Markdown file per screening
  images/       Stills used by the site
  extra/        CNAME and robots.txt, copied to the site root
theme/rerooting/
  templates/    Jinja2 templates
    partials/   Shared macros + the signup form
  static/       CSS and JS
scripts/        Trailer frame extraction
pelicanconf.py  Site content strings + settings + template helpers
publishconf.py  Production overrides
```

The theme has no build step, no framework and no third-party JavaScript. The
only external requests a visitor makes are to Google Fonts, and to YouTube —
and YouTube only once they press play on the trailer.
