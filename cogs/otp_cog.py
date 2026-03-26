import logging
from datetime import datetime

import discord
import pyotp
from discord import app_commands
from discord.ext import commands

from settings import OTP_KEY

totp = pyotp.TOTP(OTP_KEY)


def otp():
    otp = totp.now()
    now = datetime.now().timestamp()
    return discord.Embed(
        title="Google 帳號 OTP",
        description=f"你的 OTP 是：```{otp}```\n將在 <t:{int(now // totp.interval + 1) * totp.interval}:R> 過期",
        color=discord.Color.blue(),
    )


class RefreshingBtn(discord.ui.Button):
    def __init__(self):
        super().__init__(
            # emoji="",
            label="刷新 OTP",
            style=discord.ButtonStyle.primary,
            custom_id="refresh_otp",
        )

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.edit_message(embed=otp(), view=view)


refreshing_btn = RefreshingBtn()
view = discord.ui.View(timeout=None)
view.add_item(refreshing_btn)


class OTPCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="otp", description="生成用於 Google 帳號登入的一次性密碼"
    )
    async def otp(self, interaction: discord.Interaction):
        await interaction.response.send_message(embed=otp(), view=view)


async def setup(bot: commands.Bot):
    await bot.add_cog(OTPCog(bot))
    bot.add_view(view)
    logging.info(f"{__name__} 已載入")
