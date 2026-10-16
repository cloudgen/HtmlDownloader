# =============================================================================
# Open a saved page in Visual Studio Code or the default browser.
# requirement-python-oop — class PageOpen.
# Edit is hidden when the code command and the Visual Studio Code desktop
# entry are both missing. View is hidden when no default browser is set.
# =============================================================================
from __future__ import annotations

import os
import shlex
import shutil
import subprocess
import sys
from pathlib import Path


class PageOpenError(Exception):
    """The saved page cannot be opened. The message is safe to show."""

    def __init__(self, message="", logger=None):
        super().__init__(message)
        self.logger = logger
        if logger is not None:
            logger.log_message("instantiated", component="PageOpenError")


class PageOpen:
    """Open one saved index.html in Visual Studio Code or the default browser.

    Edit is available when `code` is on PATH, or when a Visual Studio Code
    desktop entry can run. View is available when the default browser is set.
    A missing tool is omitted from the menu.
    """

    CODE_DESKTOPS = (
        "code.desktop",
        "code_code.desktop",
        "visual-studio-code.desktop",
        "com.visualstudio.code.desktop",
    )

    def __init__(
        self,
        logger=None,
        which=None,
        run_text=None,
        desktop_file=None,
        browser_command=None,
        runner=None,
        platform_name=None,
    ):
        self.logger = logger
        if logger is not None:
            logger.log_message("instantiated", component="PageOpen")
        self._which = which if which is not None else shutil.which
        self._run_text = run_text if run_text is not None else self._command_text
        self._desktop_lookup = desktop_file
        self._browser_command = browser_command
        self._runner = runner if runner is not None else self._spawn
        self._platform = platform_name or sys.platform
        self._spec_cache = None

    def visual_code_path(self) -> str:
        """General Purpose: PATH location of the code command, or empty."""
        found = self._which("code")
        return found or ""

    def visual_code_installed(self) -> bool:
        """General Purpose: True when Visual Studio Code can open a file."""
        if self.visual_code_path():
            return True
        return bool(self._code_desktop())

    def default_browser_installed(self) -> bool:
        """General Purpose: True when a default browser can open a page."""
        if self._browser_command is not None:
            return bool(list(self._browser_command() or []))
        return self._spec().get("kind") != "none"

    def actions(self) -> tuple:
        """General Purpose: edit, view, or both, for tools that are installed."""
        found = []
        if self.visual_code_installed():
            found.append("edit")
        if self.default_browser_installed():
            found.append("view")
        return tuple(found)

    def edit(self, path) -> None:
        """General Purpose: Open index.html in Visual Studio Code."""
        if not os.path.isfile(path):
            raise PageOpenError("The saved page is not on disk.")
        target = os.path.abspath(path)
        exe = self.visual_code_path()
        if exe:
            self._launch([exe, target], "edit {0}".format(target))
            return
        desktop = self._code_desktop()
        if not desktop:
            raise PageOpenError("Visual Studio Code is not installed.")
        uri = Path(target).as_uri()
        argv = self._exec_argv(desktop, target, uri, prefer_file=True)
        if not argv:
            raise PageOpenError("Visual Studio Code is not installed.")
        self._launch(argv, "edit {0}".format(target))

    def view(self, path) -> None:
        """General Purpose: Open index.html in the default browser."""
        if not os.path.isfile(path):
            raise PageOpenError("The saved page is not on disk.")
        target = os.path.abspath(path)
        uri = Path(target).as_uri()
        if self._browser_command is not None:
            command = list(self._browser_command() or [])
            if not command:
                raise PageOpenError("No default browser is installed.")
            if command[0] == "startfile":
                self._startfile(uri, target)
                return
            self._launch(command + [uri], "view {0}".format(target))
            return
        spec = self._spec()
        kind = spec.get("kind")
        if kind == "startfile":
            self._startfile(uri, target)
            return
        if kind == "argv":
            self._launch(list(spec.get("prefix") or []) + [uri], "view {0}".format(target))
            return
        if kind == "desktop":
            argv = self._exec_argv(spec.get("path") or "", target, uri, prefer_file=False)
            if not argv:
                xdg = self._which("xdg-open")
                if xdg:
                    argv = [xdg, uri]
            if argv:
                self._launch(argv, "view {0}".format(target))
                return
        raise PageOpenError("No default browser is installed.")

    def _launch(self, argv, message) -> None:
        if self.logger is not None:
            self.logger.log_message(message, component="PageOpen")
        try:
            self._runner(argv)
        except OSError as exc:
            raise PageOpenError(exc.strerror or "The program could not be started.")

    def _spawn(self, argv) -> None:
        subprocess.Popen(
            argv,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True,
        )

    def _startfile(self, uri, target) -> None:
        start = getattr(os, "startfile", None)
        if start is None:
            raise PageOpenError("No default browser is installed.")
        if self.logger is not None:
            self.logger.log_message("view {0}".format(target), component="PageOpen")
        try:
            start(uri)
        except OSError as exc:
            raise PageOpenError(exc.strerror or "No default browser is installed.")

    def _spec(self) -> dict:
        if self._spec_cache is None:
            self._spec_cache = self._load_spec()
        return self._spec_cache

    def _load_spec(self) -> dict:
        """How to open the default browser. kind none means it is not installed."""
        named = os.environ.get("BROWSER")
        if named is not None and named.strip() != "":
            command = self._browser_from_env(named)
            if command:
                return {"kind": "argv", "prefix": command}
            return {"kind": "none"}
        if self._platform == "darwin":
            path = self._which("open") or ""
            if path:
                return {"kind": "argv", "prefix": [path]}
            return {"kind": "none"}
        if self._platform == "win32":
            if self._windows_progid():
                return {"kind": "startfile"}
            return {"kind": "none"}
        desktop = self._freedesktop_browser()
        if desktop:
            return {"kind": "desktop", "path": desktop}
        return {"kind": "none"}

    def _browser_from_env(self, raw) -> list:
        try:
            parts = shlex.split(raw.strip())
        except ValueError:
            return []
        if not parts:
            return []
        command = parts[0]
        if os.path.isabs(command):
            if os.path.isfile(command) and os.access(command, os.X_OK):
                return parts
            return []
        found = self._which(command)
        if not found:
            return []
        return [found] + parts[1:]

    def _freedesktop_browser(self) -> str:
        for argv in (
            ["xdg-mime", "query", "default", "x-scheme-handler/http"],
            ["xdg-settings", "get", "default-web-browser"],
        ):
            if not self._which(argv[0]):
                continue
            desktop_id = self._desktop_id(self._run_text(argv))
            if not desktop_id:
                continue
            path = self._desktop_file(desktop_id)
            if path and self._desktop_runnable(path):
                return path
        return ""

    def _desktop_id(self, text) -> str:
        lines = (text or "").strip().splitlines()
        if not lines:
            return ""
        token = lines[0].strip()
        if not token.endswith(".desktop"):
            return ""
        if "/" in token or "\\" in token or token.startswith("."):
            return ""
        return token

    def _code_desktop(self) -> str:
        for name in self.CODE_DESKTOPS:
            path = self._desktop_file(name)
            if path and self._desktop_runnable(path):
                return path
        return ""

    def _desktop_file(self, desktop_id) -> str:
        if self._desktop_lookup is not None:
            found = self._desktop_lookup(desktop_id)
            return found or ""
        return self._find_desktop(desktop_id)

    def _find_desktop(self, desktop_id) -> str:
        if (
            not desktop_id
            or desktop_id != os.path.basename(desktop_id)
            or not desktop_id.endswith(".desktop")
        ):
            return ""
        folders = []
        data_home = os.environ.get("XDG_DATA_HOME", "").strip()
        home = os.environ.get("HOME", "").strip()
        if data_home:
            folders.append(os.path.join(data_home, "applications"))
        elif home:
            folders.append(os.path.join(home, ".local", "share", "applications"))
        data_dirs = os.environ.get("XDG_DATA_DIRS", "/usr/local/share:/usr/share")
        for item in data_dirs.split(os.pathsep):
            if item:
                folders.append(os.path.join(item, "applications"))
        folders.append("/var/lib/snapd/desktop/applications")
        folders.append("/var/lib/flatpak/exports/share/applications")
        if home:
            folders.append(
                os.path.join(home, ".local", "share", "flatpak", "exports", "share", "applications")
            )
        for folder in folders:
            path = os.path.join(folder, desktop_id)
            if os.path.isfile(path):
                return path
        return ""

    def _desktop_fields(self, path) -> dict:
        fields = {}
        if not path or not os.path.isfile(path):
            return fields
        try:
            with open(path, "r", encoding="utf-8", errors="replace") as handle:
                seen_header = False
                for line in handle:
                    stripped = line.strip()
                    if stripped.startswith("["):
                        if seen_header:
                            break
                        seen_header = True
                        continue
                    if not stripped or stripped.startswith("#") or "=" not in stripped:
                        continue
                    key, value = stripped.split("=", 1)
                    if key in ("Exec", "TryExec") and key not in fields:
                        fields[key] = value.strip()
        except OSError:
            return {}
        return fields

    def _desktop_runnable(self, path) -> bool:
        fields = self._desktop_fields(path)
        if not fields.get("Exec"):
            return False
        try_exec = fields.get("TryExec", "")
        if not try_exec:
            return True
        if os.path.isabs(try_exec):
            return os.path.isfile(try_exec) and os.access(try_exec, os.X_OK)
        return bool(self._which(try_exec))

    def _exec_argv(self, desktop_path, target_path, uri, prefer_file) -> list:
        fields = self._desktop_fields(desktop_path)
        command = fields.get("Exec", "")
        if not command:
            return []
        try:
            parts = shlex.split(command)
        except ValueError:
            return []
        used = False
        argv = []
        for part in parts:
            if any(token in part for token in ("%u", "%U", "%f", "%F")):
                used = True
            expanded = self._expand_field(part, target_path, uri, desktop_path)
            if expanded:
                argv.append(expanded)
        if not argv or not argv[0] or argv[0].startswith("-"):
            return []
        if not used:
            argv.append(target_path if prefer_file else uri)
        return argv

    def _expand_field(self, part, target_path, uri, desktop_path) -> str:
        if "%" not in part:
            return part
        protected = part.replace("%%", "\0")
        if protected in ("%u", "%U"):
            return uri
        if protected in ("%f", "%F"):
            return target_path
        if protected in ("%i", "%c", "%k"):
            return ""
        protected = protected.replace("%u", uri).replace("%U", uri)
        protected = protected.replace("%f", target_path).replace("%F", target_path)
        protected = protected.replace("%k", desktop_path)
        for token in ("%i", "%c", "%d", "%D", "%n", "%N", "%v", "%m"):
            protected = protected.replace(token, "")
        return protected.replace("\0", "%").strip()

    def _windows_progid(self) -> str:
        if self._platform != "win32":
            return ""
        try:
            import winreg
        except ImportError:
            return ""
        key_path = r"Software\Microsoft\Windows\Shell\Associations\UrlAssociations\http\UserChoice"
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path)
        except OSError:
            return ""
        try:
            value, _kind = winreg.QueryValueEx(key, "ProgId")
        except OSError:
            return ""
        finally:
            winreg.CloseKey(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
        return ""

    def _command_text(self, argv) -> str:
        try:
            done = subprocess.run(
                argv,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                timeout=2,
                check=False,
                text=True,
            )
        except (OSError, subprocess.TimeoutExpired):
            return ""
        if done.returncode != 0:
            return ""
        return (done.stdout or "").strip()
