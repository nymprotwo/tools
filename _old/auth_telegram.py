#!/usr/bin/env python3
"""Run once to create syntax_session.session — then copy to server."""
import asyncio
from telethon import TelegramClient

API_ID   = 36716788
API_HASH = '0d8a1d84f28a4b108116807a0738ad8f'

async def main():
    async with TelegramClient('syntax_session', API_ID, API_HASH) as client:
        me = await client.get_me()
        print(f"✅ Logged in as: {me.first_name} (@{me.username})")
        print("✅ syntax_session.session created — upload it to server!")

asyncio.run(main())
