#!/usr/bin/env python3
"""BGM Helper — port 8082. Run: python3 bgm-helper.py"""
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.request, urllib.parse, json, os, uuid, ssl, random

SONGS_DIR = os.path.expanduser("~/Desktop/MoneyPrinterTurbo/resource/songs")
FREESOUND_TOKEN = "PAH6VgVIISLgNATzMxOJ8kkhwcazmdg3YnqPGBO3"
CTX = ssl.create_default_context()
HEADERS = {"User-Agent": "nymtendo/1.0"}

GENRE_QUERIES = {
    "ambient":    "ambient background music calm",
    "cinematic":  "cinematic orchestral epic background",
    "upbeat":     "upbeat positive background music",
    "lofi":       "lofi chill relaxing",
    "nature":     "nature sounds ambient rain",
    "electronic": "electronic background beat",
}


def freesound_search(genre):
    query = GENRE_QUERIES.get(genre, genre + " background music")
    url = (
        "https://freesound.org/apiv2/search/text/"
        f"?token={FREESOUND_TOKEN}"
        f"&query={urllib.parse.quote(query)}"
        "&page_size=20&fields=id,name,duration,previews"
    )
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, context=CTX) as r:
        data = json.loads(r.read())
    results = [
        x for x in data.get("results", [])
        if x.get("previews", {}).get("preview-hq-mp3")
        and 30 <= x.get("duration", 0) <= 300
    ]
    if not results:
        return None
    pick = random.choice(results[:10])
    # use lq-mp3 (~300KB) for faster download; quality fine for background
    url = pick["previews"].get("preview-lq-mp3") or pick["previews"]["preview-hq-mp3"]
    return {"name": pick["name"], "url": url, "duration": pick["duration"]}


def download_track(mp3_url):
    os.makedirs(SONGS_DIR, exist_ok=True)
    filename = f"bgm_{uuid.uuid4().hex[:8]}.mp3"
    req = urllib.request.Request(mp3_url, headers=HEADERS)
    with urllib.request.urlopen(req, context=CTX) as r, \
         open(os.path.join(SONGS_DIR, filename), "wb") as f:
        f.write(r.read())
    return filename


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args): pass  # quiet

    def _json(self, code, data):
        body = json.dumps(data).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        params = dict(urllib.parse.parse_qsl(parsed.query))
        try:
            if parsed.path == "/proxy":
                # download from our server (fast) to local MPT songs dir
                url = params.get("url", "")
                filename = download_track(url)
                self._json(200, {"filename": filename})

            elif parsed.path == "/fetch":
                track = freesound_search(params.get("genre", "ambient"))
                if not track:
                    return self._json(404, {"error": "no tracks found"})
                filename = download_track(track["url"])
                self._json(200, {"filename": filename, "name": track["name"], "duration": track["duration"]})

            elif parsed.path == "/search":
                track = freesound_search(params.get("genre", "ambient"))
                self._json(200, track or {})

            else:
                self._json(404, {"error": "not found"})
        except Exception as e:
            self._json(500, {"error": str(e)})


if __name__ == "__main__":
    print(f"[BGM] http://localhost:8082  songs→ {SONGS_DIR}")
    HTTPServer(("localhost", 8082), Handler).serve_forever()
