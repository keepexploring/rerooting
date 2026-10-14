PY?=python3
VENV?=.venv
BIN=$(VENV)/bin
PELICAN=$(BIN)/pelican
STAMP=$(VENV)/.installed
OUTPUT=output
PORT?=8000

.PHONY: help install install-dev html serve clean publish frames

help:
	@echo "make install   - create .venv and install dependencies"
	@echo "make serve     - build and preview at http://localhost:$(PORT) (auto-reloads)"
	@echo "make html      - one-off local build into $(OUTPUT)/"
	@echo "make publish   - production build (absolute URLs, rerooting.org)"
	@echo "make frames    - re-extract still frames from the trailer"
	@echo "make clean     - remove the build output"

# A virtualenv writes its own absolute path into every console script, so .venv
# stops working the moment this folder is moved or renamed: the scripts are
# still there, but their shebang points at a Python that no longer exists (make
# then reports a baffling "No such file or directory" for a file you can see).
# So don't just check that .venv exists -- try to run it, and rebuild if it is
# missing, stale or half-installed. Paths here are all relative to the Makefile,
# which keeps the project copyable to anywhere.
install:
	@if ! $(PELICAN) --version >/dev/null 2>&1; then \
	  if [ -d $(VENV) ]; then \
	    echo "$(VENV) is unusable (moved folder?) -- rebuilding it"; \
	  else \
	    echo "Creating $(VENV)"; \
	  fi; \
	  rm -rf $(VENV); \
	  $(PY) -m venv $(VENV); \
	  $(BIN)/pip install --quiet --upgrade pip; \
	  $(BIN)/pip install --quiet -r requirements.txt; \
	  touch $(STAMP); \
	elif [ requirements.txt -nt $(STAMP) ]; then \
	  echo "requirements.txt has changed -- updating $(VENV)"; \
	  $(BIN)/pip install --quiet -r requirements.txt; \
	  touch $(STAMP); \
	fi
	@echo "Dependencies installed into $(VENV)"

# yt-dlp and ffmpeg, needed only by the frame extraction script.
install-dev: install
	@$(BIN)/pip install --quiet -r requirements-dev.txt

html: install
	$(PELICAN) content -s pelicanconf.py

serve: install
	$(PELICAN) --autoreload --listen --port $(PORT) content -s pelicanconf.py

publish: install
	$(PELICAN) content -s publishconf.py

frames: install-dev
	./scripts/extract-frames.sh

clean:
	rm -rf $(OUTPUT)
