#!/usr/bin/env python3
"""
Syntaks bot menu mapper.
Runs once, logs in, clicks every button, saves the full menu tree to syntaks_map.json
"""
import asyncio, json, time
from telethon import TelegramClient, events
from telethon.tl.types import KeyboardButtonCallback, KeyboardButtonUrl, ReplyKeyboardMarkup, ReplyInlineMarkup

API_ID   = 36716788
API_HASH = '0d8a1d84f28a4b108116807a0738ad8f'
BOT      = 'syntxaibot'
SESSION  = 'syntax_session'
OUT_FILE = 'syntaks_map.json'

# ── helpers ──────────────────────────────────────────────────────────────────

def extract_buttons(message):
    """Return list of button texts from a message."""
    if not message.reply_markup:
        return []
    rows = []
    markup = message.reply_markup
    if hasattr(markup, 'rows'):
        for row in markup.rows:
            for btn in row.buttons:
                rows.append(btn.text)
    return rows

async def get_bot_reply(client, timeout=15):
    """Wait for the next message from the bot."""
    fut = asyncio.get_event_loop().create_future()
    async def handler(event):
        if not fut.done():
            fut.set_result(event.message)
    client.add_event_handler(handler, events.NewMessage(from_users=BOT))
    try:
        return await asyncio.wait_for(fut, timeout=timeout)
    except asyncio.TimeoutError:
        return None
    finally:
        client.remove_event_handler(handler)

async def click_button(client, message, btn_text, timeout=20):
    """Click a button by text and return the bot's response message."""
    if not message.reply_markup:
        return None
    # Try inline keyboard
    for row in getattr(message.reply_markup, 'rows', []):
        for btn in row.buttons:
            if btn.text == btn_text:
                await message.click(text=btn_text)
                return await get_bot_reply(client, timeout)
    return None

# ── main mapper ───────────────────────────────────────────────────────────────

async def map_menu(client, start_message, path=[], depth=0, tree=None):
    if tree is None:
        tree = {}
    if depth > 3:  # don't go too deep
        return tree

    buttons = extract_buttons(start_message)
    key = ' > '.join(path) if path else 'ROOT'
    tree[key] = {
        'text': start_message.text[:200] if start_message.text else '',
        'buttons': buttons,
        'path': path.copy(),
    }
    print(f"{'  '*depth}[{key}] buttons: {buttons}")

    # Skip buttons that are clearly back/cancel/profile
    skip = {'◀️ Назад', 'Назад', '❌ Отмена', 'Отмена', '🔙 Назад', '⬅️ Назад'}

    for btn_text in buttons:
        if btn_text in skip:
            continue
        child_path = path + [btn_text]
        child_key = ' > '.join(child_path)
        if child_key in tree:
            continue  # already visited

        print(f"{'  '*depth}  → clicking: {btn_text}")
        response = await click_button(client, start_message, btn_text, timeout=12)
        if response is None:
            print(f"{'  '*depth}  ✗ no response")
            tree[child_key] = {'text': '', 'buttons': [], 'path': child_path, 'note': 'no_response'}
            continue

        await asyncio.sleep(1)

        # Recurse into sub-menu
        await map_menu(client, response, child_path, depth + 1, tree)

        # Go back to parent — re-send the parent button or /start
        if depth == 0:
            await client.send_message(BOT, '/start')
        else:
            # re-click parent path from root
            await client.send_message(BOT, '/start')
            await asyncio.sleep(1)
            current_msg = await get_bot_reply(client, timeout=8)
            for p_btn in path:
                if current_msg:
                    current_msg = await click_button(client, current_msg, p_btn, timeout=10)
                    await asyncio.sleep(1.5)
            start_message = current_msg  # update reference

        if start_message is None:
            break
        await asyncio.sleep(1.5)

    return tree

async def main():
    async with TelegramClient(SESSION, API_ID, API_HASH) as client:
        print("✅ Connected as:", (await client.get_me()).username)
        print("Sending /start to syntxaibot...")

        await client.send_message(BOT, '/start')
        root_msg = await get_bot_reply(client, timeout=15)

        if not root_msg:
            print("❌ No response from bot")
            return

        print(f"Root message: {root_msg.text[:100]}")
        print(f"Root buttons: {extract_buttons(root_msg)}")
        print("\nStarting menu mapping...\n")

        tree = await map_menu(client, root_msg, [], 0, {})

        with open(OUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(tree, f, ensure_ascii=False, indent=2)

        print(f"\n✅ Done! Saved {len(tree)} menu nodes to {OUT_FILE}")
        print("\n=== SUMMARY ===")
        for k, v in tree.items():
            print(f"  {k}: {v['buttons']}")

asyncio.run(main())
