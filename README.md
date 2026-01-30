# 👻 Discord Purger Selfbot v2.0

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-active-brightgreen)

> "We are defined by what we leave behind."

---

## 🇵🇱 Opis Projektu (Polish)

**Discord Purger Selfbot** to zaawansowane narzędzie CLI (Command Line Interface) oraz TUI (Terminal User Interface) przeznaczone do masowego usuwania wiadomości na Discordzie. Wyposażony w nowoczesny interfejs graficzny w terminalu (Rich Dashboard) oraz interaktywne menu wyboru, pozwala na precyzyjne czyszczenie historii czatów, monitorowanie słów kluczowych oraz automatyczne usuwanie wiadomości wybranych użytkowników.

### ✨ Główne Funkcje
- **Modern Dashboard**: Piękny, responsywny baner ASCII i status systemu na żywo.
- **Interactive TUI**: Sterowanie botem za pomocą strzałek w terminalu (wybór serwera, kanału i celu).
- **Smart Purge Engine**: Inteligentne czyszczenie z obsługą Rate Limitów (429) i dynamicznymi opóźnieniami.
- **Precyzyjne Filtry**: Usuwanie po słowie, użytkowniku, załącznikach, linkach lub dacie.
- **Global Purge**: Możliwość czyszczenia wiadomości danego użytkownika na całym serwerze jednocześnie.
- **Whitelist Protection**: Ochrona ważnych wiadomości przed przypadkowym usunięciem.

---

## 🇬🇧 Project Description (English)

**Discord Purger Selfbot** is an advanced CLI/TUI tool designed for bulk message deletion on Discord. Featuring a modern Rich Dashboard and an interactive selection menu, it allows for pinpoint chat history cleaning, keyword monitoring, and automated user-specific message removal.

### ✨ Key Features
- **Modern Dashboard**: Stunning, responsive ASCII banner and live system status.
- **Interactive TUI**: Control the bot using arrow keys in your terminal (select server, channel, and target).
- **Smart Purge Engine**: Intelligent cleaning with Rate Limit (429) handling and dynamic delays.
- **Precision Filters**: Delete by keyword, user, attachments, links, or date.
- **Global Purge**: Clean a specific user's messages across the entire server at once.
- **Whitelist Protection**: Protect important messages from accidental deletion.

---

## ⚙️ Instalacja / Installation

### 1. Wymagania / Requirements
- **Python 3.8.x** lub nowszy.
- Token konta Discord (Selfbot Token).

### 2. Pobieranie / Download
```bash
git clone https://github.com/YOUR_USERNAME/Discord-Purger-Selfbot.git
cd Discord-Purger-Selfbot
```

### 3. Konfiguracja / Configuration
Skopiuj plik `.env.example` na `.env` i wpisz swój token:
```bash
cp .env.example .env
# Edytuj plik .env i wklej token / Edit .env and paste your token
```
*Alternatywnie stwórz plik `token.txt` i wklej w nim sam token.*

### 4. Instalacja Zależności / Install Dependencies
**Windows:**
```bash
setup_purger.bat
```
**Linux / macOS:**
```bash
chmod +x setup_purger.sh
./setup_purger.sh
```

---

## 🚀 Jak używać / How to use

Uruchom bota poleceniem:
```bash
python purger_bot.py
```

### Wybór Interfejsu / Interface Choice:
1. **Interactive Menu**: Naciśnij **ENTER** w konsoli, aby otworzyć wizualny kreator. Wybierz serwer, kanał i opcję czyszczenia za pomocą strzałek.
2. **Discord Commands**: Wpisz komendy bezpośrednio na wybranym kanale Discord (widoczne tylko dla Ciebie).

---

## 📜 Komendy / Command Reference

Wszystkie komendy zaczynają się od kropki (`.`).

| Komenda / Command | Opis (PL) | Description (EN) |
| :--- | :--- | :--- |
| `.purge_user <ID/@user>` | Usuwa wiadomości wybranego użytkownika. | Purge messages from a specific user. |
| `.purge_word <słowo>` | Usuwa wiadomości zawierające dane słowo. | Delete messages containing a keyword. |
| `.purge_media` | Usuwa wiadomości z załącznikami (obrazy/filmy). | Remove messages with attachments/media. |
| `.purge_links` | Usuwa wiadomości zawierające linki URL. | Clear messages containing URLs. |
| `.purge_since <YYYY-MM-DD>` | Usuwa wiadomości wysłane po danej dacie. | Delete messages sent after a specific date. |
| `.purge_user_all <ID>` | Czyści użytkownika na **wszystkich** kanałach. | Purge user across **all** server channels. |
| `.watch_user <ID>` | Automatycznie usuwa każdą nową wiadomość usera. | Toggle auto-delete for every new message. |
| `.watch_word <słowo>` | Automatycznie usuwa każde użycie słowa. | Toggle word monitoring/auto-deletion. |
| `.whitelist <ID>` | Dodaje wiadomość do listy chronionej. | Add a message ID to the safe list. |
| `.speed <safe/fast/insane>` | Zmienia szybkość usuwania (delay). | Adjust deletion delay/speed. |
| `.multipurge` | Masowe czyszczenie wielu kanałów. | Bulk deletion across multiple channels. |
| `.stop` | Natychmiast zatrzymuje trwający proces. | Emergency stop for any active operation. |
| `.shutdown` | Bezpiecznie wylogowuje i wyłącza bota. | Secure logout and shutdown. |

---

## ⚠️ Ostrzeżenie / Disclaimer

**Używasz tego narzędzia na własną odpowiedzialność.** Selfboty są naruszeniem Warunków Korzystania z Usługi Discord (ToS). Nadużywanie bota może prowadzić do zawieszenia konta. Bot został zaprojektowany z myślą o bezpieczeństwie (dynamiczne opóźnienia), ale zawsze zachowaj ostrożność.

**Use this tool at your own risk.** Selfbots violate Discord's Terms of Service (ToS). Overusing the bot may lead to account suspension. This bot is designed with safety in mind (dynamic delays), but always exercise caution.

---

## 🤝 Autor / Author
Stworzone przez **GH0ST** (@GH0ST-codes-pl)
