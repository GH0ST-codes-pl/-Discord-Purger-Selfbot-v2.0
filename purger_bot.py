import discord
from discord.ext import commands
import os
import asyncio
import logging
import re
import sys
import io
from datetime import datetime
from dotenv import load_dotenv

# Force UTF-8 encoding and safe error handling for terminal output
os.environ['PYTHONIOENCODING'] = 'utf-8'
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.logging import RichHandler
from rich.text import Text
from rich.align import Align
from rich.console import Group
from rich.layout import Layout
from rich.columns import Columns
from rich.live import Live
import questionary



# Initialize Rich Console with safe encoding
console = Console(force_terminal=True)

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

def clean_text(text):
    """Radically remove surrogates for safe terminal output."""
    if not isinstance(text, str):
        text = str(text)
    # This manually filters out lone surrogates (0xD800 - 0xDFFF)
    return "".join(c for c in text if not (0xD800 <= ord(c) <= 0xDFFF))

def draw_dashboard(bot_user):
    broom_ascii = r"""
                ||
                ||
                ||
                ||
                ||
                ||
                ||
         _______||_______
        /@@@@@@@@@@@@@@@@\
       /@@@@@@@@@@@@@@@@@@\
      |@@@@@@@@@@@@@@@@@@@@|
      |@@@@@@@@@@@@@@@@@@@@|
       \@@@@@@@@@@@@@@@@@@/
        \________________/
    """
    
    title_ascii = r"""
 ██████╗ ██╗   ██╗██████╗  ██████╗ ███████╗██████╗ 
 ██╔══██╗██║   ██║██╔══██╗██╔════╝ ██╔════╝██╔══██╗
 ██████╔╝██║   ██║██████╔╝██║  ███╗█████╗  ██████╔╝
 ██╔═══╝ ██║   ██║██╔══██╗██║   ██║██╔══╝  ██╔══██╗
 ██║     ╚██████╔╝██║  ██║╚██████╔╝███████╗██║  ██║
 ╚═╝      ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝
    """
    
    quote_panel = Panel(
        Align.center("[bold bright_yellow]\"We are defined by what we leave behind.\"[/bold bright_yellow]"),
        border_style="yellow",
        padding=(0, 2),
        title="[bold white]Motto[/bold white]",
        title_align="center"
    )
    
    header = Group(
        Align.center(f"[bold magenta]{title_ascii}[/bold magenta]"),
        Align.center(f"[white]{broom_ascii}[/white]"),
        Align.center(quote_panel),
        Align.center("\n[bold cyan]>> ADVANCED DISCORD PURGER SYSTEM v2.0 <<[/bold cyan]"),
        Align.center("[bold yellow]Security Protocol Active | Managed by GH0ST[/bold yellow]")
    )

    # Commands Table
    cmd_table = Table(show_header=True, header_style="bold cyan", border_style="dim", box=None)
    cmd_table.add_column("Command", style="magenta")
    cmd_table.add_column("Description", style="white")
    
    cmd_table.add_row(".purge_user", "Clear user or @everyone")
    cmd_table.add_row(".purge_word", "Delete messages with word")
    cmd_table.add_row(".purge_media", "Delete attachments/media")
    cmd_table.add_row(".purge_links", "Delete messages with URLs")
    cmd_table.add_row(".purge_since", "Delete since YYYY-MM-DD")
    cmd_table.add_row(".purge_user_all", "Global user purge (Server)")
    cmd_table.add_row(".watch_user", "Toggle auto-user-delete")
    cmd_table.add_row(".watch_word", "Toggle word monitoring")
    cmd_table.add_row(".whitelist", "Manage safe messages")
    cmd_table.add_row(".speed", "Set delay (safe/fast/...)")
    cmd_table.add_row(".multipurge", "Cross-channel deletion")
    cmd_table.add_row(".stop", "Stop active operation")
    cmd_table.add_row(".shutdown", "Secure logout")

    # Status Info
    status_info = f"""
[cyan]Logged In As:[/cyan] [bold white]{clean_text(bot_user)}[/bold white]
[cyan]Current Delay:[/cyan] [bold yellow]{deletion_delay}s[/bold yellow]
[cyan]Monitoring:[/cyan] [bold red]{clean_text(target_user_id) if target_user_id else 'Inactive'}[/bold red]
[cyan]Whitelisted IDs:[/cyan] [bold green]{len(whitelist_ids)}[/bold green]
[cyan]Session Start:[/cyan] [white]{datetime.now().strftime('%H:%M:%S')}[/white]
    """

    # Printing Dashboard
    console.print(Panel(header, border_style="magenta", padding=(1, 2)))
    
    # Body Columns
    body = Columns([
        Panel(cmd_table, title="[bold magenta]Control Deck[/bold magenta]", border_style="magenta", padding=(1, 2), expand=True),
        Panel(status_info.strip(), title="[bold cyan]System Status[/bold cyan]", border_style="cyan", padding=(1, 2), expand=True)
    ], equal=True, expand=True)
    
    console.print(body)

# Load environment variables (mostly for legacy or other config)
load_dotenv()


def get_token():
    """Tries to load token from token.txt or .env file."""
    token_file = "token.txt"
    if os.path.exists(token_file):
        with open(token_file, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    return line
    return os.getenv("DISCORD_BOT_TOKEN")


# Selfbot configuration
bot = commands.Bot(command_prefix=".", self_bot=True)

# Global configuration state
target_user_id = None
watched_words = []
whitelist_ids = set()
deletion_delay = 2.2 # Default safe delay
cancel_purge = False # Global flag for stopping ongoing operations

URL_REGEX = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'

@bot.event
async def on_ready():
    console.clear()
    draw_dashboard(bot.user)
    console.print("")
    logger.info(f"Selfbot successfully initialized for session: {bot.user}")
    
    # Start the interactive CLI menu in the background
    asyncio.create_task(interactive_cli())

async def interactive_cli():
    """Background task for the interactive terminal menu."""
    while True:
        # We wait for user input (Enter) to start the menu so it doesn't interrupt the initial dashboard
        await asyncio.to_thread(input, "\n[Press ENTER to open Interactive Menu...]\n")
        
        try:
            # 1. Select Server
            guilds = {clean_text(g.name): g for g in bot.guilds}
            if not guilds:
                console.print("[yellow]No servers found.[/yellow]")
                continue
                
            guild_name = await questionary.select(
                "Select a server:",
                choices=list(guilds.keys()) + ["Cancel"]
            ).ask_async()
            
            if guild_name == "Cancel" or not guild_name:
                continue
            guild = guilds[guild_name]
            
            # 2. Select Channel
            channels = {f"#{clean_text(c.name)}": c for c in guild.text_channels}
            if not channels:
                console.print("[yellow]No text channels found in this server.[/yellow]")
                continue
                
            channel_name = await questionary.select(
                "Select a channel:",
                choices=list(channels.keys()) + ["Back"]
            ).ask_async()
            
            if channel_name == "Back" or not channel_name:
                continue
            channel = channels[channel_name]
            
            # 3. Select Action
            action = await questionary.select(
                "What would you like to do?",
                choices=[
                    "Purge Messages from a Specific User",
                    "Purge Messages from Everyone",
                    "Purge Messages by Word/Phrase",
                    "Back"
                ]
            ).ask_async()
            
            if action == "Back" or not action:
                continue
            
            filter_func = None
            target_desc = ""
            
            if action == "Purge Messages from a Specific User":
                search_query = await questionary.text("Search for User (name or ID part):").ask_async()
                if search_query is None: continue
                
                # Search logic
                found_users = []
                seen_ids = set() # Safe way to track uniqueness
                query_lower = search_query.lower()
                
                # 1. Check Guild Members (if cached)
                if guild.members:
                    for m in guild.members:
                        if query_lower in m.name.lower() or query_lower in str(m.id):
                            if m.id not in seen_ids:
                                found_users.append(m)
                                seen_ids.add(m.id)
                
                # 2. Scan a bit of history to find more users
                if len(found_users) < 10:
                    console.print(f"[dim]Searching channel history for '{clean_text(search_query)}'...[/dim]")
                    async for m in channel.history(limit=200):
                        if query_lower in m.author.name.lower() or query_lower in str(m.author.id):
                            if m.author.id not in seen_ids:
                                found_users.append(m.author)
                                seen_ids.add(m.author.id)
                        if len(found_users) >= 20: break
                
                if not found_users:
                    console.print(f"[yellow]No users found matching '{clean_text(search_query)}'. Try ID manually.[/yellow]")
                    user_choices = ["Enter User ID Manually", "Back"]
                else:
                    user_choices = [f"{clean_text(u.name)} ({u.id})" for u in found_users]
                    user_choices.append("Enter User ID Manually")
                    user_choices.append("Back")
                
                user_pick = await questionary.select(
                    f"Select result for '{clean_text(search_query)}':",
                    choices=user_choices
                ).ask_async()
                
                if user_pick == "Back" or not user_pick:
                    continue
                
                if user_pick == "Enter User ID Manually":
                    user_id_str = await questionary.text("Enter User ID:").ask_async()
                    try:
                        target_id = int(user_id_str)
                        filter_func = lambda m: m.author.id == target_id
                        target_desc = f"User ID {target_id}"
                    except:
                        console.print("[red]Invalid User ID.[/red]")
                        continue
                else:
                    target_id = int(user_pick.split("(")[-1].strip(")"))
                    filter_func = lambda m: m.author.id == target_id
                    target_desc = user_pick.split(" (")[0]
                    
            elif action == "Purge Messages from Everyone":
                filter_func = lambda m: True
                target_desc = "EVERYONE"
                
            elif action == "Purge Messages by Word/Phrase":
                phrase = await questionary.text("Enter word or phrase to delete:").ask_async()
                if not phrase:
                    continue
                filter_func = lambda m: phrase.lower() in m.content.lower()
                target_desc = f"Word: '{phrase}'"

            # 4. Settings
            limit_str = await questionary.text("How many messages to scan? (default 1000):", default="1000").ask_async()
            limit = int(limit_str) if limit_str.isdigit() else 1000
            
            # 5. Confirmation
            confirm = await questionary.confirm(
                f"Ready to purge {target_desc} in #{clean_text(channel.name)}? (Scan: {limit} messages)"
            ).ask_async()
            
            if confirm:
                console.print(f"[bold cyan]--- INTERACTIVE PURGE STARTED: {target_desc} in #{clean_text(channel.name)} ---[/bold cyan]")
                
                # We need to simulate a context for smart_purge
                # Create a simple class to mimic ctx
                class MockCtx:
                    def __init__(self, chan):
                        self.channel = chan
                        # Use guild.me (Member object) for proper permission checks if in a guild
                        self.author = chan.guild.me if hasattr(chan, "guild") and chan.guild else bot.user
                
                mock_ctx = MockCtx(channel)
                s_count, d_count = await smart_purge(
                    mock_ctx,
                    channel.history(limit=limit),
                    filter_func=filter_func
                )
                
                msg = f"✅ Finished! Deleted {d_count} messages. (Scanned {s_count})"
                console.print(f"[bold green]{clean_text(msg)}[/bold green]")
                
        except Exception as e:
            console.print(f"[bold red]Interactive Menu Error: {clean_text(str(e))}[/bold red]")

    

async def smart_purge(ctx, history_iterator, scanned_limit=None, filter_func=None):
    """
    Unified purging logic with rate-limit handling, whitelist protection, 
    dynamic delays, and permission auto-detection.
    """
    global whitelist_ids, deletion_delay, cancel_purge
    cancel_purge = False # Reset flag when a new purge starts
    scanned_count = 0
    deleted_count = 0
    
    # \ud83d\udd75\ufe0f Permission Check: Can we delete other people's messages?
    permissions = ctx.channel.permissions_for(ctx.author)
    can_manage = permissions.manage_messages or permissions.administrator
    
    if not can_manage:
        console.print("[bold yellow]\u26a0\ufe0f No 'Manage Messages' permission! Switching to PERSONAL MODE (clearing only your own content).[/bold yellow]")

    async for message in history_iterator:
        if cancel_purge:
            console.print("[bold yellow]\ud83d\uded1 Purge operation cancelled by user.[/bold yellow]")
            break
            
        scanned_count += 1
        
        # Stop if we hit the limit
        if scanned_limit and scanned_count > scanned_limit:
            break
            
        if scanned_count % 100 == 0:
            console.print(f"[blue]\ud83d\udce1 Scanned {scanned_count} messages...[/blue]", end="\r")

        # Whitelist protection
        if message.id in whitelist_ids:
            continue

        # Logic: If no admin perms, we ONLY delete OUR messages, even if filter_func matches.
        # If we have admin perms, we follow the filter_func exactly.
        is_own_message = message.author.id == bot.user.id
        
        if filter_func(message):
            if can_manage or is_own_message:
                try:
                    await message.delete()
                    deleted_count += 1
                    
                    # Truncate content for cleaner output (increased limit for readability)
                    content = (message.content[:500] + '...') if len(message.content) > 500 else message.content
                    content = content.replace("\n", " ") # Keep it on one line
                    
                    chan_name = message.channel.name if hasattr(message.channel, "name") else "DM"
                    safe_content = clean_text(content)
                    console.print(f"[bold red]🔥 [DELETE][/bold red] [cyan]#{deleted_count}[/cyan] [dim]|[/dim] [green]#{clean_text(chan_name)}[/green] [dim]|[/dim] [white]{safe_content}[/white]")
                    await asyncio.sleep(deletion_delay)
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
                        console.print(f"[bold red]❌ API Error: {clean_text(str(e))}[/bold red]")
                    
    return scanned_count, deleted_count

@bot.event
async def on_message(message):
    global target_user_id, watched_words, whitelist_ids
    
    # Pre-check: Never auto-delete whitelisted messages
    if message.id in whitelist_ids:
        await bot.process_commands(message)
        return

    # 1. Auto-delete new messages from the targeted user
    is_everyone = target_user_id == "everyone"
    is_target_user = target_user_id and message.author.id == target_user_id
    
    if (is_everyone or is_target_user) and message.author.id != bot.user.id:
        try:
            await message.delete()
            mode_label = "EVERYONE" if is_everyone else "USER"
            
            # Truncate content for cleaner output
            content = (message.content[:500] + '...') if len(message.content) > 500 else message.content
            content = content.replace("\n", " ")
            
            console.print(f"[bold red]\ud83d\udd25 [AUTO-DELETE-{mode_label}][/bold red] [cyan]{message.author}[/cyan] [dim]|[/dim] [white]{content}[/white]")
        except:
            pass
            
    # 2. Auto-delete messages containing watched words
    content_lower = message.content.lower()
    for word in watched_words:
        if word.lower() in content_lower:
            try:
                await message.delete()
                
                # Truncate content for cleaner output
                disp_content = (message.content[:500] + '...') if len(message.content) > 500 else message.content
                disp_content = disp_content.replace("\n", " ")
                
                console.print(f"[bold red]\ud83d\udd25 [WATCH-WORD][/bold red] '[yellow]{word}[/yellow]' [dim]|[/dim] [cyan]{message.author}[/cyan] [dim]|[/dim] [white]{disp_content}[/white]")
                break # One deletion is enough
            except:
                pass

    await bot.process_commands(message)

@bot.command(name="watch_user")
async def watch_user(ctx, user_input: str = None):
    global target_user_id
    
    try:
        await ctx.message.delete()
    except:
        pass
        
    # Check for "everyone" or "@everyone"
    is_everyone = user_input and user_input.lower() in ["everyone", "@everyone"]
    
    if user_input is None or (not is_everyone and target_user_id == user_input):
        # Reset if no input or toggling off specific user ID string (legacy check)
        target_user_id = None
        console.print("[bold yellow]\ud83d\uded1 Stopped monitoring.[/bold yellow]")
        return

    if is_everyone:
        if target_user_id == "everyone":
            target_user_id = None
            console.print("[bold yellow]\ud83d\uded1 Stopped monitoring everyone.[/bold yellow]")
        else:
            target_user_id = "everyone"
            console.print("[bold green]\ud83d\udc40 Started monitoring EVERYONE.[/bold green]")
        return

    # Try to resolve user
    try:
        # Check if it's a mention or ID
        converter = commands.UserConverter()
        user = await converter.convert(ctx, user_input)
        
        if target_user_id == user.id:
            target_user_id = None
            console.print(f"[bold yellow]\ud83d\uded1 Stopped monitoring user: {user.name}[/bold yellow]")
        else:
            target_user_id = user.id
            console.print(f"[bold green]\ud83d\udc40 Started monitoring user: {user.name}[/bold green]")
    except commands.BadArgument:
        console.print(f"[bold red]\u274c Could not find user: {user_input}[/bold red]")


@bot.command(name="watch_word")
async def watch_word(ctx, word: str = None):
    global watched_words
    
    try:
        await ctx.message.delete()
    except:
        pass
        
    if word is None:
        console.print(f"[cyan]\ud83d\udccb Currently watched words: {', '.join(watched_words) or 'None'}[/cyan]")
        return

    if word.lower() in [w.lower() for w in watched_words]:
        watched_words = [w for w in watched_words if w.lower() != word.lower()]
        console.print(f"\ud83d\uded1 Stopped monitoring word: {word}")
    else:
        watched_words.append(word)
        console.print(f"\ud83d\udc40 Started monitoring word: {word}")

@bot.command(name="purge_user")
async def purge_user(ctx, arg1: str = None, arg2: str = None):
    """
    Delete messages from a specific user or everyone.
    Usage: .purge_user <@User|everyone> [limit] OR .purge_user [limit]
    """
    try:
        await ctx.message.delete()
    except:
        pass

    target_input = arg1
    limit_input = arg2
    
    # Logic to handle swapped arguments or missing arguments
    # Case 1: .purge_user (no args) -> purge me, default 1000
    if target_input is None:
        target_input = str(ctx.author.id)
        limit_input = 1000
    # Case 2: .purge_user 100 -> arg1 is "100", arg2 is None
    elif target_input.isdigit() and limit_input is None:
        limit_input = int(target_input)
        target_input = str(ctx.author.id)
    # Case 3: .purge_user everyone 100
    else:
        # Try to parse limit from arg2, fallback to 1000
        try:
            limit_input = int(limit_input) if limit_input else 1000
        except ValueError:
            # Maybe it's .purge_user 100 everyone?
            if target_input.isdigit():
                temp = target_input
                target_input = limit_input
                limit_input = int(temp)
            else:
                limit_input = 1000

    is_everyone = target_input and target_input.lower() in ["everyone", "@everyone"]
    
    target_user = None
    if not is_everyone:
        try:
            converter = commands.UserConverter()
            target_user = await converter.convert(ctx, target_input)
        except commands.BadArgument:
            console.print(f"[bold red]\u274c Could not find user: {target_input}[/bold red]")
            return

    target_name = "EVERYONE" if is_everyone else target_user.name
    actual_limit = limit_input if limit_input > 0 else None
    
    console.print(f"[bold cyan]--- STARTED PURGE FOR {target_name} ({actual_limit or 'ALL'}) ---[/bold cyan]")
    
    def filter_func(m):
        if is_everyone:
            return True
        return m.author.id == target_user.id

    s_count, d_count = await smart_purge(
        ctx, 
        ctx.channel.history(limit=actual_limit), 
        filter_func=filter_func
    )

    msg = f"\u2705 Deleted {d_count} messages from {target_name} (Scanned {s_count})"
    console.print(f"[bold green]{msg}[/bold green]")

@bot.command(name="purge_word")
async def purge_word(ctx, word: str, limit: int = 1000):
    actual_limit = limit if limit > 0 else None

    try:
        await ctx.message.delete()
    except:
        pass

    console.print(f"[bold cyan]--- STARTED PURGE FOR WORD: '{word}' ---[/bold cyan]")
    
    s_count, d_count = await smart_purge(
        ctx, 
        ctx.channel.history(limit=actual_limit), 
        filter_func=lambda m: word.lower() in m.content.lower()
    )

    msg = f"\u2705 Deleted {d_count} messages containing '{word}' (Scanned {s_count})"
    console.print(f"[bold green]{msg}[/bold green]")

@bot.command(name="purge_media")
async def purge_media(ctx, limit: int = 1000):
    actual_limit = limit if limit > 0 else None

    try:
        await ctx.message.delete()
    except:
        pass

    console.print(f"[bold cyan]--- STARTED PURGE FOR MEDIA/ATTACHMENTS ---[/bold cyan]")
    
    s_count, d_count = await smart_purge(
        ctx, 
        ctx.channel.history(limit=actual_limit), 
        filter_func=lambda m: len(m.attachments) > 0
    )

    msg = f"\u2705 Deleted {d_count} messages with media (Scanned {s_count})"
    console.print(f"[bold green]{msg}[/bold green]")

@bot.command(name="purge_links")
async def purge_links(ctx, limit: int = 1000):
    actual_limit = limit if limit > 0 else None

    try:
        await ctx.message.delete()
    except:
        pass

    console.print(f"[bold cyan]--- STARTED PURGE FOR LINKS ---[/bold cyan]")
    
    s_count, d_count = await smart_purge(
        ctx, 
        ctx.channel.history(limit=actual_limit), 
        filter_func=lambda m: re.search(URL_REGEX, m.content)
    )

    msg = f"\u2705 Deleted {d_count} messages with links (Scanned {s_count})"
    console.print(f"[bold green]{msg}[/bold green]")

@bot.command(name="purge_since")
async def purge_since(ctx, date_str: str, limit: int = 1000):
    try:
        since_date = datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        console.print("\u274c Invalid format! Use: `.purge_since YYYY-MM-DD`")
        return

    actual_limit = limit if limit > 0 else None

    try:
        await ctx.message.delete()
    except:
        pass

    console.print(f"[bold cyan]--- STARTED PURGE SINCE {date_str} ---[/bold cyan]")
    
    s_count, d_count = await smart_purge(
        ctx, 
        ctx.channel.history(limit=actual_limit, after=since_date), 
        filter_func=lambda m: True # All messages after date
    )

    msg = f"\u2705 Deleted {d_count} messages since {date_str} (Scanned {s_count})"
    console.print(f"[bold green]{msg}[/bold green]")

@bot.command(name="whitelist")
async def whitelist(ctx, action: str = "list", message_id: int = None):
    global whitelist_ids
    
    try:
        await ctx.message.delete()
    except:
        pass

    if action == "add" and message_id:
        whitelist_ids.add(message_id)
        msg = f"\ud83d\udee1\ufe0f Added message `{message_id}` to whitelist."
    elif action == "remove" and message_id:
        whitelist_ids.discard(message_id)
        msg = f"\ud83d\udace Removed message `{message_id}` from whitelist."
    elif action == "clear":
        whitelist_ids.clear()
        msg = "\ud83d\uddf3 Whitelist cleared."
    else:
        msg = f"\ud83d\udccb Current Whitelist: {', '.join(map(str, whitelist_ids)) or 'Empty'}"

    console.print(msg)

@bot.command(name="speed")
async def speed(ctx, mode: str = "safe"):
    global deletion_delay
    
    try:
        await ctx.message.delete()
    except:
        pass

    modes = {
        "safe": 2.2,
        "fast": 1.2,
        "insane": 0.5
    }

    if mode in modes:
        deletion_delay = modes[mode]
    else:
        try:
            deletion_delay = float(mode)
        except ValueError:
            console.print("\u274c Usage: `.speed <safe/fast/insane/float>`")
            return

    msg = f"\u26a1 Speed set to: {mode} ({deletion_delay}s delay)"
    console.print(f"[bold yellow]{msg}[/bold yellow]")

@bot.command(name="multipurge")
async def multipurge(ctx, *channels: discord.TextChannel):
    if not channels:
        console.print("\u274c Usage: `.multipurge #chan1 #chan2 ...`")
        return

    try:
        await ctx.message.delete()
    except:
        pass

    console.print(f"[bold cyan]--- STARTED MULTI-CHANNEL PURGE ({len(channels)} channels) ---[/bold cyan]")
    
    total_deleted = 0
    for channel in channels:
        if cancel_purge:
            break
            
        chan_display = channel.name if hasattr(channel, "name") else f"DM ({channel.recipient})"
        console.print(f"[magenta]\ud83c\udf10 Purging channel: {chan_display}...[/magenta]")
        try:
            _, d_count = await smart_purge(
                ctx, 
                channel.history(limit=1000), # Default limit for multipurge
                filter_func=lambda m: m.author.id == bot.user.id
            )
            total_deleted += d_count
        except Exception as e:
            console.print(f"[red]\u274c Error in {channel.name}: {e}[/red]")

    msg = f"\u2705 MULTI-PURGE FINISHED! Deleted {total_deleted} messages across {len(channels)} channels."
    console.print(f"[bold green]{msg}[/bold green]")

@bot.command(name="purge_user_all")
async def purge_user_all(ctx, target_input: str):
    """
    Delete all messages from a specific user across all text channels in the server.
    Usage: .purge_user_all <@User|UserID>
    """
    try:
        await ctx.message.delete()
    except:
        pass

    try:
        converter = commands.UserConverter()
        target_user = await converter.convert(ctx, target_input)
    except commands.BadArgument:
        console.print(f"[bold red]\u274c Could not find user: {target_input}[/bold red]")
        return

    if not ctx.guild:
        console.print("[bold red]\u274c This command can only be used in a server.[/bold red]")
        return

    console.print(f"[bold cyan]--- STARTED GLOBAL PURGE FOR USER: {target_user.name} ---[/bold cyan]")
    
    total_deleted = 0
    channels_processed = 0
    
    # Get all text channels in the guild
    text_channels = ctx.guild.text_channels
    
    for channel in text_channels:
        if cancel_purge:
            break
            
        # Check permissions for each channel
        permissions = channel.permissions_for(ctx.author)
        can_manage = permissions.manage_messages or permissions.administrator
        
        # If we can't manage messages, we can only delete our OWN messages (but that's already handled in smart_purge)
        # However, for a user-specific purge, if we don't have manage_messages, we can ONLY delete our own
        # so if target_user != bot.user, we skip unless we have permissions.
        
        if not can_manage and target_user.id != bot.user.id:
            continue
            
        console.print(f"[magenta]🌐 Scanning channel: #{clean_text(channel.name)}...[/magenta]")
        try:
            _, d_count = await smart_purge(
                ctx, 
                channel.history(limit=None), # Scans all history
                filter_func=lambda m: m.author.id == target_user.id
            )
            total_deleted += d_count
            channels_processed += 1
        except Exception as e:
            console.print(f"[red]❌ Error in #{clean_text(channel.name)}: {clean_text(str(e))}[/red]")

    msg = f"✅ GLOBAL PURGE FINISHED! Deleted {total_deleted} messages from {clean_text(target_user.name)} across {channels_processed} channels."
    console.print(f"[bold green]{clean_text(msg)}[/bold green]")

@bot.command(name="shutdown")
async def shutdown(ctx):
    try:
        await ctx.message.delete()
    except:
        pass

    msg = "\ud83d\udc4b Selfbot is shutting down. Goodbye!"
    console.print(f"\n[bold magenta]{'='*40}[/bold magenta]")
    console.print(f"[bold magenta]   {msg}   [/bold magenta]")
    console.print(f"[bold magenta]{'='*40}[/bold magenta]\n")
    
    await bot.close()

@bot.command(name="stop")
async def stop_purge(ctx):
    global cancel_purge
    cancel_purge = True
    
    try:
        await ctx.message.delete()
    except:
        pass
        
    msg = "\ud83d\uded1 Requested purge cancellation..."
    console.print(f"[bold yellow]{msg}[/bold yellow]")

@bot.event
async def on_command_error(ctx, error):
    error_msg = ""
    if isinstance(error, commands.UserNotFound):
        error_msg = "\u274c User not found."
    elif isinstance(error, commands.MissingRequiredArgument):
        error_msg = "\u274c Missing argument. Check `.on_ready` for command list."
    elif isinstance(error, commands.ChannelNotFound):
        error_msg = "\u274c Channel not found."
    elif isinstance(error, commands.BadArgument):
        error_msg = "\u274c Bad argument. Make sure ID or mention is correct."
    else:
        error_msg = f"❌ Command error: {clean_text(str(error))}"
    
    console.print(error_msg)
    
    try:
        await ctx.message.delete()
    except:
        pass

if __name__ == "__main__":
    token = get_token()
    
    if not token:
        # Professional setup screen for first-time users
        console.clear()
        setup_header = Panel(
            Align.center("[bold cyan]DISCORD PURGER - INITIAL SETUP[/bold cyan]\n[white]No token found in token.txt or .env[/white]"),
            border_style="cyan",
            padding=(1, 2)
        )
        console.print(setup_header)
        
        token = questionary.password(
            "Please enter your Discord User Token (it will be saved to token.txt):"
        ).ask()
        
        if token:
            with open("token.txt", "w") as f:
                f.write(token.strip())
            console.print("[bold green]✅ Token successfully saved to token.txt![/bold green]")
        else:
            console.print("[bold red]❌ No token provided. System shutdown.[/bold red]")
            sys.exit(1)
            
    try:
        bot.run(token)
    except discord.LoginFailure:
        console.print(f"\n[bold red]{'='*60}[/bold red]")
        console.print("[bold red]CRITICAL LOGIN FAILURE![/bold red]")
        console.print("[white]The token provided is invalid or expired.[/white]")
        console.print("[yellow]Possible reasons:[/yellow]")
        console.print("[dim]1. You provided a BOT token instead of a USER token.[/dim]")
        console.print("[dim]2. You enabled 2FA and need to use the token from your browser.[/dim]")
        console.print("[dim]3. The token in 'token.txt' is corrupted.[/dim]")
        console.print("\n[bold cyan]Action:[/bold cyan] Delete 'token.txt' and restart the bot to re-enter.")
        console.print(f"[bold red]{'='*60}[/bold red]\n")
    except Exception as e:
        console.print(f"[bold red]Unexpected startup error: {clean_text(str(e))}[/bold red]")
