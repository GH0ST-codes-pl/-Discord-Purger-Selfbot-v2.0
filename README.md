# 👻 Discord Purger Selfbot v2.0

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-active-brightgreen)

> "We are defined by what we leave behind."

---

## 🇵🇱 Opis Projektu / 🇬🇧 Project Description

**[PL]** **Discord Purger Selfbot** to zaawansowane narzędzie do masowego usuwania wiadomości, wyposażone w nowoczesny interfejs graficzny w terminalu (Rich Dashboard) oraz interaktywne menu wyboru. Pozwala na precyzyjne czyszczenie historii, monitorowanie słów kluczowych oraz automatyczne usuwanie wiadomości wybranych użytkowników.

**[EN]** **Discord Purger Selfbot** is an advanced bulk message deletion tool featuring a modern Rich Dashboard and an interactive selection menu. It allows for precision history cleaning, keyword monitoring, and automated user-specific message removal.

---

### ✨ Główne Funkcje / Key Features

| Funkcja (PL) | Description (EN) |
| :--- | :--- |
| **Nowoczesny Dashboard** | Stunning, responsive ASCII banner and live system status. |
| **Interaktywne Menu TUI** | Control the bot using arrow keys (select server, channel, and target). |
| **Inteligentny Silnik** | Smart cleaning with Rate Limit (429) handling and dynamic delays. |
| **Precyzyjne Filtry** | Delete by keyword, user, attachments, links, or date. |
| **Globalne Czyszczenie** | Clean a specific user's messages across the entire server at once. |
| **Ochrona Whitelist** | Protect important messages from accidental deletion. |

---

## ⚙️ Instalacja / Installation

### 1. Wymagania / Requirements
- **Python 3.8+**
- **[PL]** Token konta Discord (Selfbot Token). / **[EN]** Discord Account Token (Selfbot Token).

### 2. Pobieranie / Download
```bash
git clone https://github.com/GH0ST-codes-pl/-Discord-Purger-Selfbot-v2.0.git
cd -Discord-Purger-Selfbot-v2.0
```

### 3. Konfiguracja / Configuration
**[PL]** Skopiuj plik `.env.example` na `.env` i wpisz swój token:
**[EN]** Copy the `.env.example` file to `.env` and enter your token:
```bash
cp .env.example .env
```

### 4. Instalacja Zależności / Install Dependencies
**Windows:**
```bash
setup_purger.bat
```
**Linux / macOS:**
```bash
chmod +x setup_purger.sh
././setup_purger.sh
```

**Android (Termux):**
```bash
pkg update && pkg upgrade
pkg install python git
pip install -r requirements_purger.txt
python purger_bot.py
```

---

## 🚀 Jak używać / How to use

**[PL]** Uruchom bota poleceniem: / **[EN]** Run the bot using:
```bash
python purger_bot.py
```

### 🎮 Interakcja / Interaction:

**1. [PL] Interaktywne Menu:** Naciśnij **ENTER** w konsoli, aby otworzyć wizualny kreator. Wybierz serwer, kanał i opcję za pomocą strzałek.
**1. [EN] Interactive Menu:** Press **ENTER** in the console to open the visual guide. Select server, channel, and options using arrow keys.

**2. [PL] Komendy Discord:** Wpisz komendy bezpośrednio na kanał (widoczne tylko dla Ciebie).
**2. [EN] Discord Commands:** Type commands directly in any channel (visible only to you).

---

## 📜 Komendy / Command Reference

| Komenda / Command | Opis (PL) | Description (EN) |
| :--- | :--- | :--- |
| `.purge_user <ID/@user>` | Usuwa wiadomości wybranego użytkownika. | Purge messages from a specific user. |
| `.purge_word <słowo>` | Usuwa wiadomości zawierające dane słowo. | Delete messages containing a keyword. |
| `.purge_media` | Usuwa wiadomości z załącznikami. | Remove messages with attachments/media. |
| `.purge_links` | Usuwa wiadomości zawierające linki URL. | Clear messages containing URLs. |
| `.purge_since <YYYY-MM-DD>` | Wiadomości po danej dacie. | Messages after a specific date. |
| `.purge_user_all <ID>` | Czyści usera na całym serwerze. | Purge user across the entire server. |
| `.watch_user <ID>` | Auto-usuwanie wiadomości usera. | Toggle user auto-deletion. |
| `.watch_word <słowo>` | Auto-usuwanie słowa/frazy. | Toggle word monitoring/auto-delete. |
| `.whitelist <ID>` | Dodaje wiadomość do listy chronionej. | Add a message ID to the safe list. |
| `.speed <safe/fast/insane>` | Zmienia szybkość (delay). | Adjust deletion delay/speed. |
| `.stop` | Natychmiastowe zatrzymanie. | Emergency stop for any operation. |
| `.shutdown` | Bezpieczne wyłączenie bota. | Secure logout and shutdown. |

---

## ⚠️ Ostrzeżenie / Disclaimer

**[PL]** **Używasz tego narzędzia na własną odpowiedzialność.** Selfboty naruszają ToS Discorda. Nadużywanie może prowadzić do zawieszenia konta. Bot ma wbudowane bezpieczne opóźnienia, ale zawsze zachowaj ostrożność.

**[EN]** **Use this tool at your own risk.** Selfbots violate Discord's ToS. Overusing it may lead to account suspension. The bot features built-in safety delays, but always exercise caution.

---

## 🤝 Autor / Author
Created by **GH0ST** (@GH0ST-codes-pl)
