# YouTube Regengeräusche Downloader

Ein Tool zum Herunterladen von Regengeräuschen und anderen Hintergrundgeräuschen von YouTube und zur Konvertierung in MP3-Dateien, die optional auf einen USB-Stick kopiert werden können.

## Funktionen

- Herunterladen von YouTube-Videos mit Regengeräuschen
- Konvertierung in MP3-Format
- Automatische Erkennung und Kopieren auf USB-Sticks
- Konfigurierbare Einstellungen

## Installation

1. Stelle sicher, dass Python 3.9 oder höher installiert ist
2. Klone dieses Repository oder lade es herunter
3. Installiere die Abhängigkeiten:

```bash
pip install -r requirements.txt
```

4. Stelle sicher, dass FFmpeg auf deinem System installiert ist

## Verwendung

```bash
python main.py --url "https://www.youtube.com/watch?v=YOUTUBE_VIDEO_ID"
```

Weitere Optionen:

```bash
python main.py --help
```

## Konfiguration

Die Konfiguration kann in der Datei `config/config.json` angepasst werden.

## Lizenz

Dieses Projekt ist unter der MIT-Lizenz lizenziert.