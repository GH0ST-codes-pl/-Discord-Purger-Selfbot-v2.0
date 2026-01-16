# 🧹 Discord Message Purger Selfbot

![CLI Preview](preview.png)

A professional, high-performance Discord selfbot for deep message cleanup. It features a beautiful CLI, advanced scanning capabilities, and real-time monitoring.

> [!CAUTION]
> **DISCLAIMER**: Using self-bots is against Discord's Terms of Service. This tool is for educational purposes only. Use it at your own risk; your account may be permanently banned.

## ✨ Features

- **Deep History Scanning**: Traverse entire channel histories without arbitrary limits.
- **Word Purging**: Delete all messages containing specific keywords or phrases.
- **Thread Support**: Automatically scans and cleans up messages within active threads.
- **Stealth Mode**: Operations are completely silent on the channel; command invocations are immediately deleted.
- **Auto-Delete (Watch Mode)**: Real-time monitoring and immediate deletion of new messages from a target user.
- **Safe Rate Limiting**: Intelligent delays and automatic retry logic to minimize 429 errors.
- **Rich CLI**: A beautiful, colorful terminal interface with real-time feedback.
- **Private Reporting**: Get detailed execution summaries delivered straight to your DMs.

## 🛠️ Installation

### 📱 Android (Termux)
1. **Prepare Environment**:
   ```bash
   pkg update && pkg upgrade
   pkg install python git
   ```
2. **Clone and Setup**:
   ```bash
   git clone https://github.com/GH0ST-codes-pl/Discord-Purger-Selfbot.git
   cd Discord-Purger-Selfbot
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements_purger.txt
   ```

### 🍎 macOS / 🐧 Linux
1. **Clone the repository**:
   ```bash
   git clone https://github.com/GH0ST-codes-pl/Discord-Purger-Selfbot.git
   cd Discord-Purger-Selfbot
   ```
2. **Run Setup Script**:
   ```bash
   chmod +x setup_purger.sh
   ./setup_purger.sh
   ```

### 🪟 Windows
1. **Clone the repository**:
   ```powershell
   git clone https://github.com/GH0ST-codes-pl/Discord-Purger-Selfbot.git
   cd Discord-Purger-Selfbot
   ```
2. **Run Setup Script**:
   - Double-click `setup_purger.bat` or run it via CMD/PowerShell.

### ⚙️ Configuration (All Platforms)
1. Rename `.env.example` to `.env`.
2. Insert your **User Token** into `DISCORD_BOT_TOKEN`.
3. *Tutorial: [How to get Discord Token](https://www.youtube.com/results?search_query=how+to+get+discord+user+token)*.

## 🚀 Usage

### macOS / Linux / Termux:
```bash
./venv/bin/python purger_bot.py
```

### Windows:
```powershell
venv\Scripts\python purger_bot.py
```

### Commands

| Command | Usage | Description |
| :--- | :--- | :--- |
| `.purge_user` | `.purge_user [@User] [limit]` | Deletes messages from a user. If none, cleans your own. Set limit to `0` for full scan. |
| `.purge_word` | `.purge_word <word> [limit]` | Deletes messages containing a specific word. Set limit to `0` for full scan. |
| `.watch_user` | `.watch_user @User` | Toggles real-time auto-deletion of new messages from @User. |

### Przykłady (Examples)
- `.purge_user @Troll 0` — Completely wipes every message from @Troll in the current channel and its threads.
- `.purge_word "bad word" 0` — Deletes all messages containing "bad word".
- `.watch_user @Target` — Starts silently deleting any new message @Target posts.

## 💖 Support

If you find this tool helpful, you can support the developer via Tipply:
[Tipply - @daily-shoty](https://tipply.pl/@daily-shoty)

---
*Created by [GH0ST](https://github.com/GH0ST-codes-pl)*
