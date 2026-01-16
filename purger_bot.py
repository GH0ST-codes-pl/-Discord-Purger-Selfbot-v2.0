import discord
from discord.ext import commands
import os
import asyncio
import logging
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.logging import RichHandler
from rich.text import Text

# Initialize Rich Console
console = Console()

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s',
    datefmt="[%X]",
    handlers=[
        logging.FileHandler('purger_selfbot.log'),
        RichHandler(console=console, rich_tracebacks=True)
    ]
)
logger = logging.getLogger("purger")

def draw_banner():
    banner_text = """
    [magenta]
    ██████╗ ██╗   ██╗██████╗  ██████╗ ███████╗██████╗ 
    ██╔══██╗██║   ██║██╔══██╗██╔════╝ ██╔════╝██╔══██╗
    ██████╔╝██║   ██║██████╔╝██║  ███╗█████╗  ██████╔╝
    ██╔═══╝ ██║   ██║██╔══██╗██║   ██║██╔══╝  ██╔══██╗
    ██║     ╚██████╔╝██║  ██║╚██████╔╝███████╗██║  ██║
    ╚═╝      ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝
    [/magenta]
    [cyan]        >> DISCORD MESSAGE PURGER SELFBOT << [/cyan]
    """
    console.print(Panel(banner_text.strip(), border_style="magenta"))

# Load environment variables
load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

# Selfbot configuration
bot = commands.Bot(command_prefix=".", self_bot=True)

# Global variable for automatic user monitoring (Auto-Delete)
target_user_id = None

@bot.event
async def on_ready():
    draw_banner()
    
    table = Table(title="Available Commands", show_header=True, header_style="bold cyan")
    table.add_column("Command", style="magenta", no_wrap=True)
    table.add_column("Usage", style="green")
    table.add_column("Description", style="white")
    
    table.add_row(".purge_user", ".purge_user @User [limit]", "Delete messages from user (0=full)")
    table.add_row(".purge_word", ".purge_word <word> [limit]", "Delete messages containing word (0=full)")
    table.add_row(".watch_user", ".watch_user @User", "Toggle real-time auto-deletion")
    
    console.print(table)
    console.print(f"[bold green]Selfbot logged in as {bot.user}[/bold green]\n")
    logger.info(f"Selfbot logged in as {bot.user}")

@bot.event
async def on_message(message):
    global target_user_id
    
    # Auto-delete new messages from the targeted user if monitoring is active
    if target_user_id and message.author.id == target_user_id:
        try:
            await message.delete()
            console.print(f"[bold red]🔥 [AUTO-DELETE][/bold red] Deleted message from [cyan]{message.author}[/cyan] in #[yellow]{message.channel}[/yellow]")
        except:
            pass
            
    await bot.process_commands(message)

@bot.command(name="watch_user")
async def watch_user(ctx, user: discord.User = None):
    global target_user_id
    
    try:
        await ctx.message.delete()
    except:
        pass
        
    if user is None or (target_user_id == user.id):
        target_user_id = None
        print("🛑 Stopped automatic monitoring.")
        await ctx.author.send("🛑 Real-time monitoring disabled.")
    else:
        target_user_id = user.id
        print(f"👀 Started monitoring user: {user.name}")
        await ctx.author.send(f"👀 Real-time monitoring enabled for: {user.name}. Type `.watch_user` again to disable.")

@bot.command(name="purge_user")
async def purge_user(ctx, user: discord.User = None, limit: int = 1000):
    """
    Deletes messages from a specific user.
    If no user is specified, it cleans your own messages.
    """
    target = user or ctx.author
    actual_limit = limit if limit > 0 else None
    limit_text = f"limit: {limit}" if actual_limit else "NO LIMIT (full history scan)"

    try:
        await ctx.message.delete()
    except:
        pass

    console.print(f"[bold cyan]--- STARTED DEEP CLEANUP FOR {target.name} ({limit_text}) ---[/bold cyan]")
    
    scanned_count = 0
    deleted_count = 0
    
    async def process_messages(history_iterator, target_id=None, keyword=None):
        nonlocal scanned_count, deleted_count
        async for message in history_iterator:
            scanned_count += 1
            
            if scanned_count % 100 == 0:
                console.print(f"[blue]📡 Scanned {scanned_count} messages...[/blue]", end="\r")

            should_delete = False
            if target_id and message.author.id == target_id:
                should_delete = True
            elif keyword and keyword.lower() in message.content.lower():
                should_delete = True

            if should_delete:
                try:
                    await message.delete()
                    deleted_count += 1
                    console.print(f"[bold red]🔥 [DELETE] #{deleted_count}[/bold red] ([dim]Scanned: {scanned_count}[/dim])")
                    
                    # Safe delay for selfbots
                    await asyncio.sleep(2.2)
                    
                except discord.HTTPException as e:
                    if e.status == 429:
                        wait_time = e.retry_after + 2
                        console.print(f"[bold yellow]⚠️ Rate limit hit! Waiting {wait_time:.2f}s...[/bold yellow]")
                        await asyncio.sleep(wait_time)
                        try: # Retry once after waiting
                            await message.delete()
                            deleted_count += 1
                        except: pass
                    else:
                        console.print(f"[bold red]❌ API Error: {e}[/bold red]")

    try:
        # 1. Scan main channel history
        await process_messages(ctx.channel.history(limit=actual_limit), target_id=target.id)
        
        # 2. Scan threads if no limit is set
        if hasattr(ctx.channel, 'threads') and not actual_limit:
            console.print(f"[magenta]🧵 Checking threads in channel: {ctx.channel.name}...[/magenta]")
            for thread in ctx.channel.threads:
                await process_messages(thread.history(limit=None), target_id=target.id)

        msg_text = f"✅ FINISHED! Deleted **{deleted_count}** messages from {target.name} (Scanned {scanned_count} total messages on {ctx.channel.name})."
        console.print(f"\n[bold green]{msg_text}[/bold green]")
        logger.info(msg_text)
        
        try:
            await ctx.author.send(msg_text)
        except:
            pass
            
    except Exception as e:
        console.print(f"[bold red]❌ Critical error during scan: {e}[/bold red]")
        logger.error(f"Critical Error: {e}")

@bot.command(name="purge_word")
async def purge_word(ctx, word: str, limit: int = 1000):
    """
    Deletes messages containing a specific word.
    """
    actual_limit = limit if limit > 0 else None
    limit_text = f"limit: {limit}" if actual_limit else "NO LIMIT (full history scan)"

    try:
        await ctx.message.delete()
    except:
        pass

    console.print(f"[bold cyan]--- STARTED DEEP CLEANUP FOR WORD: '{word}' ({limit_text}) ---[/bold cyan]")
    
    scanned_count = 0
    deleted_count = 0
    
    async def process_messages(history_iterator, keyword=None):
        nonlocal scanned_count, deleted_count
        async for message in history_iterator:
            scanned_count += 1
            
            if scanned_count % 100 == 0:
                console.print(f"[blue]📡 Scanned {scanned_count} messages...[/blue]", end="\r")

            if keyword and keyword.lower() in message.content.lower():
                try:
                    await message.delete()
                    deleted_count += 1
                    console.print(f"[bold red]🔥 [DELETE] #{deleted_count}[/bold red] ([dim]Scanned: {scanned_count}[/dim])")
                    await asyncio.sleep(2.2)
                except discord.HTTPException as e:
                    if e.status == 429:
                        wait_time = e.retry_after + 2
                        console.print(f"[bold yellow]⚠️ Rate limit hit! Waiting {wait_time:.2f}s...[/bold yellow]")
                        await asyncio.sleep(wait_time)
                        try:
                            await message.delete()
                            deleted_count += 1
                        except: pass
                    else:
                        console.print(f"[bold red]❌ API Error: {e}[/bold red]")

    try:
        await process_messages(ctx.channel.history(limit=actual_limit), keyword=word)
        
        if hasattr(ctx.channel, 'threads') and not actual_limit:
            console.print(f"[magenta]🧵 Checking threads in channel: {ctx.channel.name}...[/magenta]")
            for thread in ctx.channel.threads:
                await process_messages(thread.history(limit=None), keyword=word)

        msg_text = f"✅ FINISHED! Deleted **{deleted_count}** messages containing '{word}' (Scanned {scanned_count} total messages on {ctx.channel.name})."
        console.print(f"\n[bold green]{msg_text}[/bold green]")
        logger.info(msg_text)
        
        try:
            await ctx.author.send(msg_text)
        except:
            pass
            
    except Exception as e:
        console.print(f"[bold red]❌ Critical error during scan: {e}[/bold red]")
        logger.error(f"Critical Error: {e}")

@bot.event
async def on_command_error(ctx, error):
    error_msg = ""
    if isinstance(error, commands.UserNotFound):
        error_msg = "❌ User not found."
    elif isinstance(error, commands.MissingRequiredArgument):
        error_msg = "❌ Usage: `.purge_user @User [limit]`, `.purge_word <word> [limit]` or `.watch_user @User`"
    else:
        error_msg = f"❌ Command error: {error}"
    
    print(error_msg)
    try:
        await ctx.author.send(error_msg)
    except:
        pass
    
    try:
        await ctx.message.delete()
    except:
        pass

if __name__ == "__main__":
    if TOKEN:
        try:
            bot.run(TOKEN)
        except discord.LoginFailure:
            print("CRITICAL: Login failed. Make sure DISCORD_BOT_TOKEN in .env is your USER TOKEN, not a bot token.")
    else:
        print("CRITICAL: Missing DISCORD_BOT_TOKEN in .env file")
