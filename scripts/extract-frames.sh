#!/usr/bin/env bash
#
# Pull still frames out of the trailer for use as site imagery.
#
#   ./scripts/extract-frames.sh                   # download + dump candidates
#   ./scripts/extract-frames.sh preset            # rebuild all site imagery
#   ./scripts/extract-frames.sh 00:01:12.5 hero   # grab one frame as hero.jpg
#
# Candidates land in scripts/.trailer/frames/ (git-ignored) along with contact
# sheets so you can eyeball them. Chosen frames go to content/images/.
#
# Needs yt-dlp and ffmpeg. Both come from requirements-dev.txt, so
# `make frames` is enough -- no Homebrew or Xcode required.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
WORK="$ROOT/scripts/.trailer"
VIDEO="$WORK/trailer.mp4"
FRAMES="$WORK/frames"
SHEETS="$WORK/sheets"
IMAGES="$ROOT/content/images"
VENV="$ROOT/.venv"
URL="${TRAILER_URL:-https://www.youtube.com/watch?v=q0MAijKW7ZQ}"

# Prefer the project venv, fall back to anything already on PATH.
if [[ -x "$VENV/bin/yt-dlp" ]]; then
  YTDLP="$VENV/bin/yt-dlp"
else
  YTDLP="$(command -v yt-dlp || true)"
fi

if [[ -x "$VENV/bin/python" ]] && "$VENV/bin/python" -c "import imageio_ffmpeg" 2>/dev/null; then
  FFMPEG="$("$VENV/bin/python" -c 'import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())')"
else
  FFMPEG="$(command -v ffmpeg || true)"
fi

if [[ -z "$YTDLP" || -z "$FFMPEG" ]]; then
  echo "yt-dlp and/or ffmpeg are missing. Run: make install" >&2
  exit 1
fi

mkdir -p "$WORK" "$FRAMES" "$SHEETS" "$IMAGES"

# The trailer is 1920x1080 with the 2.35:1 image letterboxed inside it, so
# every still gets the black bars cropped off first. Re-run `cropdetect` if a
# future trailer is framed differently:
#   ffmpeg -ss 60 -i trailer.mp4 -frames:v 40 -vf cropdetect -f null -
CROP="crop=1920:816:0:132"

download() {
  if [[ -f "$VIDEO" ]]; then
    echo "Trailer already downloaded: $VIDEO"
    return
  fi
  echo "Downloading trailer..."
  "$YTDLP" -f 'bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080]' \
    --merge-output-format mp4 --ffmpeg-location "$FFMPEG" -o "$VIDEO" "$URL"
}

grab() { # grab <timestamp> <output-name> <width> [quality]
  local ts="$1" name="$2" width="$3" quality="${4:-3}"
  "$FFMPEG" -loglevel error -y -ss "$ts" -i "$VIDEO" -frames:v 1 \
    -vf "$CROP,scale=${width}:-2:flags=lanczos" -q:v "$quality" "$IMAGES/$name.jpg"
  echo "  $name.jpg  <- ${ts}s  (${width}px wide)"
}

# Preset mode: rebuild every image the site uses, from the frames we chose.
# Edit the timestamps here if you want different stills; everything downstream
# picks them up automatically.
if [[ "${1:-}" == "preset" ]]; then
  download
  echo "Rebuilding site imagery..."
  grab 118 hero            2400   # Glencoe: the road through the glen
  grab 118 hero-1200       1200   # smaller hero for narrow screens
  grab 146 trailer-poster  1800   # two loaded bikes on the pass
  grab 168 signup          2000   # Hebridean road threading the lochans
  grab 210 community       1800   # leading the ponies down the croft track

  # Social preview needs a 1.91:1 crop rather than the film's 2.35:1.
  "$FFMPEG" -loglevel error -y -ss 118 -i "$VIDEO" -frames:v 1 \
    -vf "$CROP,crop=1554:816:183:0,scale=1200:630:flags=lanczos" -q:v 3 \
    "$IMAGES/og.jpg"
  echo "  og.jpg  <- 118s  (1200x630 social card)"

  echo
  du -h "$IMAGES"/*.jpg | sort -k2
  exit 0
fi

# Single-frame mode: extract one precise timestamp straight into content/images.
if [[ $# -eq 2 ]]; then
  download
  grab "$1" "$2" 2400 2
  exit 0
fi

download

echo "Extracting candidate frames (one every 2s)..."
rm -f "$FRAMES"/*.jpg
"$FFMPEG" -loglevel error -y -i "$VIDEO" \
  -vf "fps=1/2,scale=960:-2:flags=lanczos" -q:v 3 "$FRAMES/frame-%03d.jpg"

echo "Building contact sheets..."
rm -f "$SHEETS"/*.jpg
"$FFMPEG" -loglevel error -y -i "$VIDEO" \
  -vf "fps=1/2,scale=400:-2:flags=lanczos,tile=4x5" -q:v 3 "$SHEETS/sheet-%02d.jpg"

COUNT=$(find "$FRAMES" -name '*.jpg' | wc -l | tr -d ' ')
echo
echo "$COUNT candidate frames in $FRAMES"
echo "Contact sheets in $SHEETS (each tile is 2s apart, reading left to right)"
echo
echo "Frame N is at timestamp (N-1)*2 seconds. To grab one at full size:"
echo "  ./scripts/extract-frames.sh 00:00:42 hero"
