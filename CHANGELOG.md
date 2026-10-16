# CHANGELOG

All notable changes to **HtmlDownloader** are documented here.  
Version SSOT: `pyproject.toml` + `src/HtmlDownloader/__init__.__version__`.

## [Unreleased]

### Removed

- Join, file listing, and FFmpeg. `join` and `list-videos` are not verbs. The program does not scan the folder for media and does not call an encoder.
- The `hello` verb and the welcome line. Menu row 1 is no longer a welcome.

### Added

- Typed verb `download`. It needs `--url` and `--name`. It saves the HTML page to `~/.app/HtmlDownloader/output/<pagename>/index.html`. Linked stylesheets go in `output/<pagename>/assets/css/`, linked scripts in `output/<pagename>/assets/js/`, and linked images in `output/<pagename>/assets/img/`. Those three folders are flat. Font files sit in `assets/css/`.
- When `output/<pagename>/index.html` already exists, the page URL is not fetched again. Stylesheets, scripts, and images named by that file are downloaded only when the file is missing. An older save that stored the page as a single file is moved to `index.html` and continued.
- `output/url-map.json` remembers each URL and page name. Menu row **1 download** lists `page name: URL` by number, or accepts a URL.
- Menu row **2 list downloaded** lists saved page names. After a page is chosen, **21 edit** opens it in Visual Studio Code when `code` is installed, and **22 view** opens it in the default browser when one is set. A tool that is not installed is left off that menu.
- Typed verb `serve`. It needs `--page-name`. `--port` defaults to **5000**. It serves `~/.app/HtmlDownloader/output/<pagename>/` on `127.0.0.1` until Ctrl+C. `index.html` is `/`.
- Menu row **3 serve** lists saved page names. After a page is chosen, the menu asks for a port. An empty port uses **5000**.
- After stylesheet and script links are rewritten to local paths, the saved HTML drops `<base>`, `xml:base`, `<link rel="canonical">`, and HTML comments.

### Changed

- Package name is **HtmlDownloader**. Console script is `html-downloader`. Version is reset to **1.0.0**.
- Front row **1** is **download**.
- Front row **6** is **self-management**. Its list is **61**–**66**. Numbers **67**–**70** are not printed.
- Front row **7** is **language**. Its list is **71**–**83**. Numbers **84**–**98** are not printed.
- Front row **4** is **System Log**. Its list is **41**–**43**. Numbers **44**–**49** are not printed.
- The about page domain line is `Download a page and its stylesheets, scripts, and images`. Self-management row 62 reads "version and this computer."
- Public source is https://github.com/cloudgen/HtmlDownloader. README screenshots are captures of this menu: language **71**–**83**, one main menu for each language, self-management **61**–**66**, about, and System Log **41**–**43**.

## [1.0.5] - 2026-10-04

### Changed

- `about` shows one page: product identity, a host check of this computer, and a star box. The page stays English. It does not probe `ffmpeg` and it does not print a pip install line.
- Self-management row 83 reads "version, FFmpeg, and this computer."
- Version is **1.0.5**. `ChronicleLogger>=1.3.1` is unchanged.
- Product README Screenshots links every picture in `screenshots/` with an absolute `https` URL. Menu pictures captured before the about page still show **1.0.4**.

## [1.0.4] - 2026-10-04

### Added

- Text menu on a terminal when `video-join` is started with no arguments. Front rows are join (1), system-log (3), language (4), self-management (8), and Exit (9). system-log lists view-log (31), clear-log (32), log-folder (33), and Back (0). language lists English through Ελληνικά (41–53) and Back (0). self-management lists version (82), about (83), version-check (84), self-update (85), self-uninstall (86), self-install (87), and Back (0).
- Menu language file `~/.local/VideoJoin/language`. `VIDEOJOIN_LANG` overrides that file for one process and does not write it. `language` is not a command-line verb.
- Typed verbs `help`, `version`, `about`, `hello`, `join`, `list-videos`, `self-install`, `version-check`, `self-update`, and `self-uninstall`.
- `ChronicleLogger` is constructed in `main` and required at `ChronicleLogger>=1.3.1`.
- Product README shows the main menu, the system-log board, the language board, and the self-management board.
- Product README PyPI version badge (`pypi.org/project/VideoJoin`).

### Changed

- Empty argv on a terminal opens that menu and does not start the join questions. With no terminal, empty argv prints help and returns 0.
- Quick Installation documents **`pip install VideoJoin`**. This tree is **1.0.4**. A registry probe on 2026-08-19 reported **1.0.3**. Checkout `pip install -e .` stays the local path.
- Join still prefers stream copy, then re-encode, and still publishes with `shutil.move`.

---

## [1.0.3] - 2026-08-09

### Added

- Same-FS staging helpers (`staging_dir_for`, `make_temp_path`) and **`promote_file` → `shutil.move`** for publishing intermediates.
- Unique temp concat list and media intermediates (no fixed cwd-only `filelist.txt` strategy).
- Product requirements set (class, domain, pipeline, CLI, coding-style, packaging, structure, errors, runtime).
- Promote gate checklist **`CL-PYTHON-SHUTIL-MOVE-PUBLISH`** (blank + filled run).

### Changed

- Join pipeline: stream-copy to temp → promote; on failure re-encode to temp → promote.
- Package public surface: `__version__` and `main` only (no phantom `ChronicleLogger` re-export from `.cli`).
- Product README rewritten for install/usage honesty (local package primary; FFmpeg system dep).

### Fixed

- Fail-closed re-encode path: non-zero FFmpeg or missing intermediate no longer prints success.
- Reject final output path equal to either source path.

### Security

- Still user-level only; no Type 1 elevation. FFmpeg invoked with argument lists (no shell string interpolation of free-form filters).

---

## [1.0.2] - prior

### Added

- Interactive two-file join with FFmpeg stream-copy and re-encode fallback.
- Package layout under `src/VideoJoin/` with console script `video-join`.

### Notes

- Earlier packaging claims may have listed broad Python support and optional Cython tooling; runtime join does not require Cython.

---

Update this file when shipping version bumps; keep body complete (no hollow TBD sections for claimed releases).
