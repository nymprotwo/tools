#!/usr/bin/env python3
"""BGM Server — runs on 62.171.167.238:8082"""
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.request, urllib.parse, json, os, uuid, ssl, random

CACHE_DIR = "/root/bgm-cache"
FREESOUND_TOKEN = os.environ.get("FREESOUND_TOKEN", "")
GEMINI_KEY = os.environ.get("GEMINI_KEY", "")
SERVER_URL = "http://62.171.167.238:8082"
CTX = ssl.create_default_context()
HEADERS = {"User-Agent": "nymtendo/1.0"}

SCRIPT_PROMPT = """You are a short-form video scriptwriter specializing in viral TikTok and Instagram Reels content.

RULES (non-negotiable):
- First sentence MUST be a hook: shocking fact, bold claim, or question that stops the scroll
- Each sentence = one visual clip — short, punchy, standalone
- ZERO filler: no "today we're going to", "let's talk about", "in this video", "welcome"
- Conversational, like telling a friend something wild
- 8–12 sentences max (45–60 seconds when spoken)
- End with a surprising punchline, stat, or call to action
- Output ONLY the narration text — no brackets, no stage directions, no titles

Topic: {topic}
Language: {lang}"""

GENRE_QUERIES = {
    "ambient":    "ambient background music calm",
    "cinematic":  "cinematic orchestral epic background",
    "upbeat":     "upbeat positive background music",
    "lofi":       "lofi chill relaxing",
    "nature":     "nature sounds ambient rain",
    "electronic": "electronic background beat",
}

os.makedirs(CACHE_DIR, exist_ok=True)


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
        if x.get("previews", {}).get("preview-lq-mp3")
        and 30 <= x.get("duration", 0) <= 300
    ]
    if not results:
        return None
    pick = random.choice(results[:10])
    return {"name": pick["name"], "url": pick["previews"]["preview-lq-mp3"], "duration": pick["duration"]}


def download_track(mp3_url):
    filename = f"bgm_{uuid.uuid4().hex[:8]}.mp3"
    filepath = os.path.join(CACHE_DIR, filename)
    req = urllib.request.Request(mp3_url, headers=HEADERS)
    with urllib.request.urlopen(req, context=CTX) as r, open(filepath, "wb") as f:
        f.write(r.read())
    return filename


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args): pass

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
            if parsed.path == "/fetch":
                genre = params.get("genre", "ambient")
                track = freesound_search(genre)
                if not track:
                    return self._json(404, {"error": "no tracks found"})
                filename = download_track(track["url"])
                file_url = f"{SERVER_URL}/file/{filename}"
                self._json(200, {"file_url": file_url, "name": track["name"], "duration": track["duration"]})

            elif parsed.path.startswith("/file/"):
                name = os.path.basename(parsed.path)
                filepath = os.path.join(CACHE_DIR, name)
                if not os.path.exists(filepath):
                    self.send_response(404); self.end_headers(); return
                self.send_response(200)
                self.send_header("Content-Type", "audio/mpeg")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.send_header("Content-Length", str(os.path.getsize(filepath)))
                self.end_headers()
                with open(filepath, "rb") as f:
                    self.wfile.write(f.read())

            elif parsed.path == "/script":
                topic = params.get("topic", "")
                lang = params.get("lang", "English")
                if not topic:
                    return self._json(400, {"error": "topic required"})
                prompt = SCRIPT_PROMPT.format(topic=topic, lang=lang)
                body = json.dumps({
                    "contents": [{"parts": [{"text": prompt}]}],
                    "generationConfig": {"temperature": 0.9, "maxOutputTokens": 2048}
                }).encode()
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_KEY}"
                req = urllib.request.Request(url, data=body, headers={**HEADERS, "Content-Type": "application/json"}, method="POST")
                with urllib.request.urlopen(req, context=CTX, timeout=30) as r:
                    resp = json.loads(r.read())
                parts = resp["candidates"][0]["content"]["parts"]
                script = "".join(p.get("text", "") for p in parts).strip()
                self._json(200, {"script": script})

            else:
                self._json(404, {"error": "not found"})
        except Exception as e:
            self._json(500, {"error": str(e)})


if __name__ == "__main__":
    print(f"[BGM Server] http://0.0.0.0:8082  cache→ {CACHE_DIR}")
    HTTPServer(("0.0.0.0", 8082), Handler).serve_forever()
