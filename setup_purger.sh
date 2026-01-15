#!/bin/bash

# Generowanie dynamicznej ścieżki do folderu bota (relatywnie do miejsca uruchomienia)
BOT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

echo "🚀 Rozpoczynam konfigurację bota w $BOT_DIR..."
cd "$BOT_DIR"

# Tworzenie venv jeśli nie istnieje
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Instalacja zależności
echo "Installing dependencies..."
./venv/bin/pip install -r requirements_purger.txt

echo "✅ Konfiguracja zakończona!"
echo "Teraz możesz uruchomić bota komendą:"
echo "cd '$BOT_DIR' && ./venv/bin/python purger_bot.py"
