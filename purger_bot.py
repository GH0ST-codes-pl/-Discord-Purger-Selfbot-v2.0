import discord
from discord.ext import commands
import os
import asyncio
import logging
from dotenv import load_dotenv

# Konfiguracja logowania
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('purger_selfbot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Wczytaj zmienne środowiskowe
load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

# Konfiguracja selfbota
bot = commands.Bot(command_prefix=".", self_bot=True)

# Globalna zmienna do monitorowania użytkownika (Auto-Delete)
target_user_id = None

@bot.event
async def on_ready():
    logger.info(f"Selfbot zalogowany jako {bot.user}")
    print(f"--- SELFBOT GOTOWY ---")
    print(f"Komendy:")
    print(f"  .purge_user @Użytkownik [limit] - Usuwa historię (0 = cała historia)")
    print(f"  .watch_user @Użytkownik         - Włącza/wyłącza automatyczne usuwanie nowych wiadomości")

@bot.event
async def on_message(message):
    global target_user_id
    if target_user_id and message.author.id == target_user_id:
        try:
            await message.delete()
            print(f"🔥 [AUTO-DELETE] Usunięto nową wiadomość od {message.author.name}")
        except:
            pass
    await bot.process_commands(message)

@bot.command(name="watch_user")
async def watch_user(ctx, user: discord.User = None):
    global target_user_id
    try: await ctx.message.delete()
    except: pass
    if user is None or (target_user_id == user.id):
        target_user_id = None
        print("🛑 Zakończono automatyczne monitorowanie.")
        await ctx.author.send("🛑 Wyłączono automatyczne usuwanie nowych wiadomości.")
    else:
        target_user_id = user.id
        print(f"👀 Rozpoczęto automatyczne monitorowanie użytkownika: {user.name}")
        await ctx.author.send(f"👀 Włączono automatyczne usuwanie nowych wiadomości od: {user.name}. Wpisz `.watch_user` ponownie, aby wyłączyć.")

@bot.command(name="purge_user")
async def purge_user(ctx, user: discord.User = None, limit: int = 1000):
    target = user or ctx.author
    actual_limit = limit if limit > 0 else None
    
    try: await ctx.message.delete()
    except: pass

    print(f"--- ROZPOCZĘTO GŁĘBOKIE CZYSZCZENIE DLA {target.name} ---")
    scanned_count = 0
    deleted_count = 0
    
    async def process_messages(history_iterator):
        nonlocal scanned_count, deleted_count
        async for message in history_iterator:
            scanned_count += 1
            if scanned_count % 1000 == 0:
                print(f"📡 Przeskanowano już {scanned_count} wiadomości...")
            if message.author.id == target.id:
                try:
                    await message.delete()
                    deleted_count += 1
                    print(f"🔥 [DELETE] {deleted_count} (przeskanowano: {scanned_count})")
                    await asyncio.sleep(2.2)
                except discord.HTTPException as e:
                    if e.status == 429:
                        wait = e.retry_after + 2
                        print(f"⚠️ Rate limit! Czekam {wait:.2f}s...")
                        await asyncio.sleep(wait)
                        try: await message.delete(); deleted_count += 1
                        except: pass
                    else:
                        print(f"❌ Błąd API: {e}")

    try:
        await process_messages(ctx.channel.history(limit=actual_limit))
        if hasattr(ctx.channel, 'threads') and not actual_limit:
            for thread in ctx.channel.threads:
                await process_messages(thread.history(limit=None))

        msg = f"✅ ZAKOŃCZONO! Usunięto **{deleted_count}** wiadomości użytkownika {target.name}."
        print(f"--- {msg} ---")
        try: await ctx.author.send(msg)
        except: pass
    except Exception as e:
        print(f"❌ Błąd: {e}")

@bot.event
async def on_command_error(ctx, error):
    try: await ctx.message.delete()
    except: pass
    print(f"❌ Błąd komendy: {error}")

if __name__ == "__main__":
    if TOKEN:
        try: bot.run(TOKEN)
        except discord.LoginFailure: print("Błąd logowania!")
    else:
        print("Brak TOKENU w .env")
