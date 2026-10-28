# Use HtmlDownloader

Read this before you run the program. You are an agent. The person asked you to save one HTML page or to serve one page that is already saved. Use the console script `html-downloader`. Do not invent a second tool.

## When you are not at a person’s terminal

Use a typed verb. Do not start `html-downloader` with no arguments. With no arguments on a terminal, the program opens a text menu and waits. That menu is for a person. It does not download a page by itself, and it does not call pip.

## Install

Name one of these when the command is missing:

```bash
pip install HtmlDownloader
```

From a checkout of this program:

```bash
pip install -e .
```

Do not pipe a downloaded script into a shell. Do not use `sudo`, `apt`, or a dedicated system user.

## Save one page

`download` needs `--url`. It does not draw the menu.

```bash
html-downloader download --url https://example.com/guide.html
```

That URL ends with `guide.html`, so the page folder is `guide` and the HTML file is `guide.html`. The files land in `~/.app/HtmlDownloader/output/guide/guide.html`.

A URL that ends with a folder name such as `xxx` saves `~/.app/HtmlDownloader/output/xxx/index.html`.

```bash
html-downloader download --url https://example.com/xxx
```

Omit `--name` only when the URL recommends the folder that way. A host-only URL does not recommend a folder. Pass `--name` or the command exits non-zero.

```bash
html-downloader download --url https://example.com/ --name example
```

`--html` chooses the HTML file name inside the page folder. Omit it to keep a stored name, or to use the name recommended from the URL. The default file is `index.html`.

```bash
html-downloader download --url https://example.com/guide.html --name docs --html page.html
```

A missing `--url` exits non-zero. Run the same command again to fill files that are still missing. Do not fetch the page URL again when the stored HTML file is already there.

The save stores that one page and the stylesheets, scripts, and images it links. Do not follow links to more HTML pages. Do not crawl a site. There is no `crawl` verb.

## Serve one saved page

`serve` needs `--page-name`. It listens on `127.0.0.1`. The default port is **5000**. `/` is the stored HTML file.

```bash
html-downloader serve --page-name example
html-downloader serve --page-name example --port 8080
```

Do not bind any other address. Ctrl+C stops the server.

## What you must not run

These are not verbs. Do not pass them:

- `hello`
- `join`
- `list-videos`
- `crawl`
- `language`

`language` is menu row 7, not a typed verb.

Do not call an encoder. Do not join media. Do not scan the working directory to list files. List downloaded is menu row **2** only. Do not invent a typed verb for that list.

## Other typed verbs

```bash
html-downloader help
html-downloader version
html-downloader about
```

`version` prints the installed version. Do not type a version number into this skill.

`self-install`, `version-check`, `self-update`, and `self-uninstall` call pip for this package. They do not use root. Leave them alone unless the person asked for that pip action. `self-uninstall` on the command line needs `--force`.
