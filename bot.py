import discord
from discord.ext import commands
import os
import time
from flask import Flask
from threading import Thread

# ====== SET YOUR ALLOWED CHANNELS HERE ======
ALLOWED_CHANNEL_IDS = {
    1344025871802961930,  # Channel 1
    1351042676157452362,  # Channel 2
    1351042877546958930  # Channel 3
}  # ✅ Add as many channel IDs as needed

# ====== BOT SETUP ======
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True  # Needed to track user messages

bot = commands.Bot(command_prefix="!", intents=intents)

# ====== XP TRACKING DATA ======
xp_tracking = {}

# XP Calculation Parameters
WORDS_PER_UNIT = 1000  # ✅ XP is based on 1000 words per unit
XP_PERCENTAGE = 0.125  # 12.5% of min XP/session
MIN_XP_BY_LEVEL = {
    1: 150,
    2: 300,
    3: 450,
    4: 475,
    5: 750,
    6: 900,
    7: 1100,
    8: 1400,
    9: 1600,
    10: 1750,
    11: 1875,
    12: 2000,
    13: 2000,
    14: 2500,
    15: 2500,
    16: 2500,
    17: 2500,
    18: 2500,
    19: 2500,
    20: 2500
}


# ====== BOT EVENTS ======
@bot.event
async def on_ready():
    print(f'✅ Logged in as {bot.user}')
    print(
        f'✅ XP tracking is enabled for channels: {ALLOWED_CHANNEL_IDS} and their threads.'
    )
    print('Ready to track XP!')


# ====== START/STOP XP TRACKING ======
@bot.command()
async def xptrack(ctx, level: int = None):
    """Starts or stops XP tracking."""
    user_id = ctx.author.id

    if level is None:
        # Start XP tracking
        if user_id in xp_tracking:
            await ctx.send(
                f"{ctx.author.mention}, XP tracking is already active!")
            return

        xp_tracking[user_id] = {
            "start_time": time.time(),
            "word_count": 0,
            "message_count": 0
        }
        await ctx.send(
            f"{ctx.author.mention}, XP tracking started! Your roleplay will now count towards XP in the allowed RP channels and their threads."
        )

    else:
        # Stop XP tracking & calculate XP
        if user_id not in xp_tracking:
            await ctx.send(
                f"{ctx.author.mention}, you haven't started XP tracking yet!")
            return

        if level not in MIN_XP_BY_LEVEL:
            await ctx.send(
                f"{ctx.author.mention}, please enter a valid level between 1 and 20."
            )
            return

        # Retrieve tracking data
        data = xp_tracking.pop(user_id)

        # Calculate XP
        min_xp = MIN_XP_BY_LEVEL[level]
        xp_per_unit = min_xp * XP_PERCENTAGE
        rp_units = data["word_count"] / WORDS_PER_UNIT
        earned_xp = int(rp_units * xp_per_unit)

        await ctx.send(
            f"{ctx.author.mention}, XP tracking ended! You have earned **{earned_xp} XP** from your RP session."
        )


# ====== TRACK MESSAGES (Fix: Now Works in ALL Specified Channels & Threads) ======
@bot.event
async def on_message(message):
    """Tracks words while XP tracking is active, including messages in allowed threads."""
    if message.author.bot:
        return

    # ✅ Check if the message is in any of the allowed channels or a thread belonging to them
    if message.channel.id in ALLOWED_CHANNEL_IDS or (
            isinstance(message.channel, discord.Thread)
            and message.channel.parent_id in ALLOWED_CHANNEL_IDS):
        user_id = message.author.id
        if user_id in xp_tracking:
            words = message.content.split()
            if len(words) >= 5:  # ✅ Requires 5 words per message
                xp_tracking[user_id]["word_count"] += len(words)
                xp_tracking[user_id]["message_count"] += 1

    await bot.process_commands(message)


# ====== KEEP BOT ALIVE (FOR UPTIMEROBOT PING) ======
app = Flask("")


@app.route("/")
def home():
    return "Bot is running!"


def run():
    app.run(host="0.0.0.0", port=8080)


Thread(target=run).start()

# ====== RUN THE BOT ======
bot.run(os.getenv("DISCORD_BOT_TOKEN"))
