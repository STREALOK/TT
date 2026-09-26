"""serve.py - serve the TT site (the public/ folder) on this computer, with live reload.

    py serve.py               then open http://127.0.0.1:8080
    py serve.py --port 9000   (another port)

An open page reloads by itself about a second after any file in public/ is saved, so an
edit shows at once. The reload snippet is added by this server while it serves;
it is never written into the files, so any other host serves them untouched.
It listens on 127.0.0.1 only: nothing outside this computer can reach it.
Ctrl+C stops it.
"""
import argparse
import http.server
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent / "public"
RELOAD = b"""<script>/* live reload - added by serve.py while serving; not part of the page */
(function () {
  var seen = null;
  setInterval(function () {
    fetch("/__version", {cache: "no-store"})
      .then(function (r) { return r.text(); })
      .then(function (v) { if (seen === null) { seen = v; } else if (v !== seen) { location.reload(); } })
      .catch(function () {});
  }, 1000);
})();
</script>
"""


def version():
    """The newest modification time of any file in public/ (dot-folders are skipped)."""
    newest = 0.0
    for folder, subfolders, files in os.walk(ROOT):
        subfolders[:] = [d for d in subfolders if not d.startswith(".")]
        for name in files:
            try:
                newest = max(newest, os.stat(os.path.join(folder, name)).st_mtime)
            except OSError:
                pass
    return repr(newest)


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def log_message(self, fmt, *args):
        if "/__version" not in (self.path or ""):
            super().log_message(fmt, *args)

    def _send(self, body, content_type):
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        url_path = self.path.split("?", 1)[0].split("#", 1)[0]
        if url_path == "/__version":
            return self._send(version().encode("ascii"), "text/plain; charset=utf-8")
        fs_path = self.translate_path(url_path)
        if os.path.isdir(fs_path) and url_path.endswith("/"):
            fs_path = os.path.join(fs_path, "index.html")
        if fs_path.endswith(".html") and os.path.isfile(fs_path):
            page = Path(fs_path).read_bytes()
            at = page.lower().rfind(b"</body>")
            page = page[:at] + RELOAD + page[at:] if at != -1 else page + RELOAD
            return self._send(page, "text/html; charset=utf-8")
        return super().do_GET()


def main():
    ap = argparse.ArgumentParser(description="Serve the TT site (public/) on this computer, with live reload.")
    ap.add_argument("--port", type=int, default=8080)
    args = ap.parse_args()
    try:
        server = http.server.ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
    except OSError as e:
        sys.exit(f"port {args.port} is busy or refused ({e}); try: py serve.py --port 9000")
    print(f"serving {ROOT} at http://127.0.0.1:{args.port}/  (Ctrl+C stops it)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("stopped")


if __name__ == "__main__":
    main()
