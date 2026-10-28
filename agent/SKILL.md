# Use HtmlCrawler

Read this before you run the program. You are an agent. The person asked you to save one HTML page, to crawl one site, or to serve one page that is already saved. Use the console script this tree installs. Do not invent a second tool.

If this card and the product law disagree, the law wins. The law files are under `docs/requirements/`. This card is the instruction sheet.

## Which command this tree accepts

The law names the console script `html-crawler` and the module `python -m HtmlCrawler`.

This tree still installs the console script `html-downloader`. The package directory is `src/HtmlDownloader`. The module that runs is `python -m HtmlDownloader`. The distribution name is `HtmlDownloader`. Use `html-downloader` on this tree.

`crawl` is a typed verb on this tree. Help lists `crawl`, `download`, and `serve`. Do not edit the program to rename the package unless the person asked for that ship-unit pass.

## When you are not at a person’s terminal

Use a typed verb. Do not start the program with no arguments. With no arguments on a terminal, the program opens a text menu and waits. That menu is for a person. It does not download a page by itself, and it does not call pip. With no terminal, no arguments print help and return 0.

## Install

When the command is missing, from a checkout of this tree:

```bash
python -m pip install -e .
```

Do not tell the person that `python -m pip install HtmlCrawler` already matches this tree. The distribution name here is `HtmlDownloader`.

Do not pipe a downloaded script into a shell. Do not use `sudo`, `apt`, or a dedicated system user.

## Save one page

`download` needs `--url` and `--name`. Both are required. It does not draw the menu. It does not take `--depth` or `--max-pages`. There is no `--html` flag.

```bash
html-downloader download --url https://example.com/ --name example
```

On this tree the page lands at `~/.app/HtmlDownloader/output/example/index.html`. The law folder, after the ship-unit pass, is `~/.app/HtmlCrawler/output/<pagename>/index.html`.

A missing `--url` or a missing `--name` exits non-zero and names the gap. The URL must be `http` or `https`, must have a host, and must not carry a username or password.

The save stores that one page and the stylesheets, scripts, images, and fonts it links. It does not follow links to more HTML pages. Run the same command again to fill files that are still missing. When `index.html` is already there, the page URL is not fetched again.

## Crawl one site

On this tree the command is:

```bash
html-downloader crawl --url https://example.com/ --name example --depth 1 --max-pages 20
```

`--url`, `--name`, `--depth`, and `--max-pages` are all required. `--depth` is an integer of 0 or more. `--max-pages` is an integer of 1 or more. Keep both bounds on every crawl. Do not leave either bound unlimited. Do not put `--depth` or `--max-pages` on `download`.

Depth 0 is the start page. The walk stays on that host. It reads `robots.txt` before any HTML page. A failed robots fetch saves no page. It waits 1 second between requests to that host. It does not run JavaScript.

A start path of `/` writes `~/.app/HtmlDownloader/output/<sitename>/index.html`. `crawl` is not a menu row. Empty arguments do not crawl.

## Serve one saved page

`serve` needs `--page-name`. It listens on `127.0.0.1`. The default port is **5000**.

```bash
html-downloader serve --page-name example
html-downloader serve --page-name example --port 8080
```

Do not bind any other address. Ctrl+C returns 0 and prints `Stopped <name>.`

## List saved pages

List downloaded is menu row **2**. It is not a typed verb. Do not invent `list` or `list-downloaded` on the command line. A person at the terminal uses the menu.

## Front menu

The front rows are 1 download, 2 list downloaded, 3 serve, 4 System Log, 6 self-management, 7 language, and 9 Exit. Rows 5 and 8 are omitted. Do not drive this menu when no person is there.

`language` is menu row **7**. It is not a typed verb.

## What you must not run

These are not verbs. Do not pass them:

- `hello`
- `join`
- `list-videos`
- `language`

Do not call an encoder. Do not join media. Do not scan the working directory to list files. Do not start a shell installer. Do not use root. Do not start a crawl that has no depth and no page cap.

## Other typed verbs

```bash
html-downloader help
html-downloader version
html-downloader about
```

`version` prints the installed version. Do not type a version number into this skill.

`self-install`, `version-check`, `self-update`, and `self-uninstall` call `python -m pip` for the distribution `HtmlDownloader`. They do not use root. Leave them alone unless the person asked for that pip action. `self-uninstall` on the command line needs `--force`. Without `--force` the command exits non-zero and the package stays installed.

```bash
html-downloader self-uninstall --force
```
