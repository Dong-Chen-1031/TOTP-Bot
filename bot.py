from rich.traceback import install

# 安裝Rich traceback
install(show_locals=True)

import asyncio
import logging
import os

import discord
from discord.ext import commands

import settings

intents = discord.Intents.all()

bot = commands.Bot(command_prefix=settings.PREFIX, intents=intents)


@bot.event
async def on_ready():
    logging.info(f"已登入為 {bot.user.name}")
    try:
        synced = await bot.tree.sync()
        logging.info(f"已同步 {len(synced)} 個斜線指令")
    except Exception as e:
        logging.error(f"同步指令失敗: {e}")


async def load_extensions_all():
    logging.info("正在載入模組...")
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")
            # logging.info(f'已載入模組: {filename[:-3]}')


async def main():
    async with bot:
        await load_extensions_all()
        await bot.start(settings.DISCORD_BOT_TOKEN)


if __name__ == "__main__":
    logging.info("啟動機器人中...")
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("機器人已停止 (KeyboardInterrupt)")
