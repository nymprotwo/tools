#!/usr/bin/env python3
"""
Syntaks Server — port 8083
Receives requests from frontend, sends to Syntaks TG bot via Telethon, returns result URL.
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
import urllib.parse, json, os, asyncio, threading, uuid, re, base64
from telethon import TelegramClient, events

API_ID   = int(os.environ.get("TG_API_ID", "36716788"))
API_HASH = os.environ.get("TG_API_HASH", "")
SESSION  = "/root/syntax_session"
BOT      = "syntxaibot"
FILES_DIR = "/root/syntaks-files"
SERVER_URL = "https://tools.nympro.studio"

os.makedirs(FILES_DIR, exist_ok=True)

IMG  = "🎨 Дизайн с ИИ"
VID  = "🎬 Видео будущего"
AUD  = "🔊 Аудио с ИИ"
AGT  = "💡 GPTs/Claude/Gemini"

# Exact button texts verified by bot scraper
BUTTON_MAP = {
    # IMAGE
    "flux":             [IMG, "♦️ FLUX"],
    "mj":               [IMG, "🌄 MJ"],
    "seedream":         [IMG, "🧿 Seedream 5.0"],
    "sora-img":         [IMG, "🌙 Sora (GPT) Image"],
    "ideogram":         [IMG, "𝐓 Ideogram v3.0"],
    "grok-img":         [IMG, "🎯 Grok Imagine"],
    "wan":              [IMG, "👾 Wan Image"],
    "luma-img":         [IMG, "🌑 Luma Image"],
    "recraft":          [IMG, "⬣ Recraft"],
    "sd":               [IMG, "🧬 Stable Diffusion"],
    "higgsfield":       [IMG, "⚛️ Higgsfield Soul"],
    "nano-banana":      [IMG, "🍌 Nano Banana PRO"],
    "kling-kolors":     [IMG, "🌈 Kling KOLORS"],
    "runway-frames":    [IMG, "🎑 Runway Frames"],
    "kling-tryon":      [IMG, "👠 Kling Try-On"],
    "face-swap":        [IMG, "🎭 Замена лица"],
    "inpaint":          [IMG, "🖌 Дорисовка"],
    "photo-pro":        [IMG, "📸 Фото Мастер"],
    "editor":           [IMG, "✂️ Редактор"],
    "magnific":         [IMG, "🔍 Magnific Upscaler"],
    "clarity":          [IMG, "🪁 Clarity Upscaler"],
    # VIDEO
    "kling":            [VID, "📼 Kling"],
    "hailuo":           [VID, "🎦 Hailuo MiniMax"],
    "seedance":         [VID, "🧿 Seedance 2.0"],
    "seedance-1":       [VID, "🧿 Seedance"],
    "veo":              [VID, "⭕ Veo"],
    "veo-flash":        [VID, "🌐 Veo Omni Flash"],
    "runway-vid":       [VID, "🎞️ RunWay"],
    "sora2":            [VID, "🌙 SORA"],
    "luma-vid":         [VID, "📽️ Luma: DM"],
    "happyhorse":       [VID, "🎠 HappyHorse"],
    "grok-vid":         [VID, "🤖 Grok Imagine"],
    "higgsfield-v":     [VID, "⚛️ Higgsfield"],
    "wan-vid":          [VID, "👾 Wan"],
    "mj-vid":           [VID, "🛸 MJ"],
    "pika":             [VID, "🤡 Pika"],
    "beeble":           [VID, "🎞️ Beeble SwitchX"],
    "topaz":            [VID, "💠 Topaz AI"],
    "heygen":           [VID, "💜 HeyGen"],
    "hedra":            [VID, "✴️ Hedra"],
    "runway-act2":      [VID, "👁️ RunWay Act-Two"],
    "did":              [VID, "🗣️ D-ID Аватары"],
    "lip-sync":         [VID, "🫦 Синхронизатор губ"],
    "higgsfield-speak": [VID, "📢 Higgsfield Speak"],
    # AUDIO
    "suno":             [AUD, "🎸 SUNO (музыка)"],
    "elevenlabs":       [AUD, "🎙️ ElevenLabs Voice"],
    "voice-clone":      [AUD, "👥 Клонирование голоса"],
    "elevenlabs-music": [AUD, "🎷 ElevenLabs Music"],
    "sound-gen":        [AUD, "🥁 Генератор звуков"],
    "video-to-audio":   [AUD, "🌊 Видео в аудио"],
    "audio-to-text":    [AUD, "👂 Аудио в текст"],
    # AGENTS
    "gpt-editor":       [AGT, "👨‍🎨 Активировать GPT Editor"],
    "gpt-chat":         [AGT, "💬 Новый диалог"],
}

# shared asyncio loop + telethon client
loop = asyncio.new_event_loop()
client = TelegramClient(SESSION, API_ID, API_HASH, loop=loop)

def run_loop():
    loop.run_forever()

threading.Thread(target=run_loop, daemon=True).start()

async def start_client():
    await client.start()
    me = await client.get_me()
    print(f"[TG] Connected as {me.first_name} @{me.username}")

asyncio.run_coroutine_threadsafe(start_client(), loop).result(timeout=20)

# Only one request can talk to the bot at a time
bot_lock = asyncio.Lock()


async def get_reply(timeout=15):
    fut = loop.create_future()
    async def handler(event):
        if not fut.done():
            fut.set_result(event.message)
    client.add_event_handler(handler, events.NewMessage(from_users=BOT))
    client.add_event_handler(handler, events.MessageEdited(from_users=BOT))
    try:
        return await asyncio.wait_for(fut, timeout=timeout)
    except asyncio.TimeoutError:
        return None
    finally:
        client.remove_event_handler(handler)

async def send_and_wait(text, timeout=10):
    await client.send_message(BOT, text)
    try:
        return await get_reply(timeout=timeout)
    except asyncio.TimeoutError:
        return None

async def navigate_to_model(model_id):
    path = BUTTON_MAP.get(model_id)
    if not path:
        return None, f"Model '{model_id}' not in button map"

    print(f"[nav] → {model_id}, path={path}", flush=True)
    await client.send_message(BOT, "🏠 В главное меню")
    msg = await get_reply(timeout=10)
    if not msg:
        print("[nav] no reply to menu, trying /start", flush=True)
        await client.send_message(BOT, "/start")
        msg = await get_reply(timeout=10)
        if not msg:
            return None, "Bot not responding"

    await asyncio.sleep(0.5)

    for btn_text in path:
        print(f"[nav] sending '{btn_text}'", flush=True)
        msg = await send_and_wait(btn_text, timeout=12)
        if not msg:
            return None, f"No response after sending: {btn_text}"
        print(f"[nav] got reply: {repr(msg.text[:80]) if msg.text else 'media'}", flush=True)
        await asyncio.sleep(0.8)

    return msg, None

async def generate(model_id, version, prompt, file_bytes=None, file_name=None):
    async with bot_lock:
        return await _generate_locked(model_id, version, prompt, file_bytes, file_name)

async def _generate_locked(model_id, version, prompt, file_bytes=None, file_name=None):
    print(f"[gen] model={model_id} version={version!r} prompt={prompt[:60]!r}", flush=True)
    msg, err = await navigate_to_model(model_id)
    if err:
        print(f"[gen] nav error: {err}", flush=True)
        return None, err

    await asyncio.sleep(0.5)

    if file_bytes:
        import io
        await client.send_file(BOT, io.BytesIO(file_bytes), file_name=file_name or "file")
        await asyncio.sleep(1.5)

    print(f"[gen] sending prompt...", flush=True)
    await client.send_message(BOT, prompt)

    start_time = loop.time()
    print(f"[gen] waiting for result...", flush=True)
    result_msg = None
    SKIP_PHRASES = ["ожидает выполнения", "одну секунду", "обрабатывается", "генерация начата", "в очереди", "⏳", "🔄"]
    while loop.time() - start_time < 600:
        remaining = 600 - (loop.time() - start_time)
        msg = await get_reply(timeout=min(60, remaining))
        if not msg:
            print(f"[gen] 60s timeout, still waiting...", flush=True)
            continue
        btns = []
        if msg.reply_markup:
            for row in getattr(msg.reply_markup, "rows", []):
                for btn in row.buttons:
                    url = getattr(btn, "url", None)
                    btns.append({"text": btn.text, "type": type(btn).__name__, "url": url})
        print(f"[gen] got msg: text={repr(msg.text[:80]) if msg.text else None}, media={bool(msg.media)}, btns={btns}", flush=True)
        if msg.media:
            result_msg = msg
            break
        if msg.text:
            urls = re.findall(r'https?://\S+', msg.text)
            if urls:
                result_msg = msg
                break
            # if bot is asking to press a button to generate, click the first non-webview button
            if "нажмите кнопку" in msg.text.lower() or "для генерации" in msg.text.lower():
                for btn_info in btns:
                    if btn_info["type"] != "KeyboardButtonSimpleWebView" and btn_info["text"] not in ("🏠 В главное меню", "⬅️ Назад"):
                        print(f"[gen] clicking gen button: {btn_info['text']}", flush=True)
                        await client.send_message(BOT, btn_info["text"])
                        break
                continue
            # skip status/progress messages and keep waiting
            low = msg.text.lower()
            if any(p in low for p in SKIP_PHRASES):
                continue
        await asyncio.sleep(0.3)

    if not result_msg:
        return None, "Timeout — bot did not send a result after 10 min"

    if result_msg.media:
        try:
            filename = f"result_{uuid.uuid4().hex[:8]}"
            doc = getattr(result_msg, 'document', None)
            if doc:
                mime = getattr(doc, 'mime_type', '')
                if 'video' in mime: filename += '.mp4'
                elif 'audio' in mime: filename += '.mp3'
                elif 'image' in mime: filename += '.jpg'
                else: filename += '.bin'
            elif getattr(result_msg, 'photo', None):
                filename += '.jpg'
            else:
                filename += '.mp4'

            filepath = os.path.join(FILES_DIR, filename)
            await result_msg.download_media(filepath)
            if os.path.exists(filepath):
                return f"{SERVER_URL}/file/{filename}", None
        except Exception:
            pass

    if result_msg.text:
        urls = re.findall(r'https?://\S+', result_msg.text)
        if urls:
            raw_url = urls[0].rstrip(').,')
            # download to local so frontend can play/download directly
            try:
                import urllib.request, ssl
                ctx = ssl.create_default_context()
                ext = raw_url.split('?')[0].rsplit('.', 1)[-1].lower()
                if ext not in ('mp4','webm','mov','jpg','jpeg','png','gif','webp','mp3','ogg','wav'):
                    ext = 'mp4'  # assume video if unknown
                filename = f"result_{uuid.uuid4().hex[:8]}.{ext}"
                filepath = os.path.join(FILES_DIR, filename)
                req = urllib.request.Request(raw_url, headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(req, context=ctx, timeout=60) as r, open(filepath, 'wb') as f:
                    f.write(r.read())
                if os.path.exists(filepath) and os.path.getsize(filepath) > 1000:
                    return f"{SERVER_URL}/file/{filename}", None
            except Exception:
                pass
            return raw_url, None  # fallback: return bot url directly
        return None, result_msg.text[:300]

    return None, "No media or URL in response"


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args): pass

    def _json(self, code, data):
        body = json.dumps(data, ensure_ascii=False).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path.startswith("/file/"):
            name = os.path.basename(parsed.path)
            filepath = os.path.join(FILES_DIR, name)
            if not os.path.exists(filepath):
                self.send_response(404); self.end_headers(); return
            ext = name.rsplit(".", 1)[-1]
            mime = {"mp4":"video/mp4","jpg":"image/jpeg","png":"image/png","mp3":"audio/mpeg"}.get(ext, "application/octet-stream")
            self.send_response(200)
            self.send_header("Content-Type", mime)
            self.send_header("Content-Length", str(os.path.getsize(filepath)))
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            with open(filepath, "rb") as f:
                self.wfile.write(f.read())
        elif parsed.path == "/models":
            self._json(200, {"models": list(BUTTON_MAP.keys())})
        else:
            self._json(404, {"error": "not found"})

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path != "/generate":
            self._json(404, {"error": "not found"}); return

        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)

        try:
            data = json.loads(body)
        except Exception:
            self._json(400, {"error": "invalid json"}); return

        model    = data.get("model", "")
        version  = data.get("version", "")
        prompt   = data.get("prompt", "")
        file_b64 = data.get("file_base64")
        file_name = data.get("file_name")

        if not model or not prompt:
            self._json(400, {"error": "model and prompt required"}); return

        file_bytes = None
        if file_b64:
            try:
                file_bytes = base64.b64decode(file_b64)
            except Exception:
                self._json(400, {"error": "invalid file_base64"}); return

        fut = asyncio.run_coroutine_threadsafe(
            generate(model, version, prompt, file_bytes, file_name), loop
        )
        try:
            url, err = fut.result(timeout=660)
        except Exception as e:
            msg = str(e) or type(e).__name__
            self._json(500, {"error": msg}); return

        if err:
            self._json(500, {"error": err})
        else:
            self._json(200, {"url": url})


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True

if __name__ == "__main__":
    print(f"[Syntaks] listening on 0.0.0.0:8083")
    ThreadedHTTPServer(("0.0.0.0", 8083), Handler).serve_forever()
