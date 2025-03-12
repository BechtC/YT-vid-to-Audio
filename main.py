#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
YouTube Regengeräusche Downloader
---------------------------------
Ein Tool zum Herunterladen von Regengeräuschen und anderen Hintergrundgeräuschen von YouTube
und zur Konvertierung in MP3-Dateien, die optional auf einen USB-Stick kopiert werden können.
"""

import argparse
import logging
import os
import sys
from pathlib import Path

# Eigene Module importieren
from src.config_manager import ConfigManager
from src.youtube_downloader import YouTubeDownloader
from src.audio_converter import AudioConverter
from src.usb_handler import USBHandler
from src.utils import setup_logging

def parse_arguments():
    """Kommandozeilenargumente parsen."""
    parser = argparse.ArgumentParser(
        description="YouTube Regengeräusche Downloader"
    )
    parser.add_argument(
        "--url", "-u", 
        type=str, 
        help="YouTube-URL des Videos"
    )
    parser.add_argument(
        "--output", "-o", 
        type=str, 
        help="Ausgabepfad für die MP3-Datei (überschreibt Konfiguration)"
    )
    parser.add_argument(
        "--usb", 
        action="store_true", 
        help="Auf USB-Stick kopieren, wenn verfügbar"
    )
    parser.add_argument(
        "--config", "-c", 
        type=str, 
        default="config/config.json", 
        help="Pfad zur Konfigurationsdatei"
    )
    parser.add_argument(
        "--verbose", "-v", 
        action="store_true", 
        help="Ausführliche Ausgabe"
    )
    
    return parser.parse_args()

def main():
    """Hauptfunktion des Programms."""
    # Argumente parsen
    args = parse_arguments()
    
    # Konfiguration laden
    config_manager = ConfigManager(args.config)
    config = config_manager.load_config()
    
    # Logging einrichten
    log_level = logging.DEBUG if args.verbose else getattr(logging, config["logging"]["level"])
    setup_logging(log_level, config["logging"]["file"])
    
    logger = logging.getLogger(__name__)
    logger.info("YouTube Regengeräusche Downloader gestartet")
    
    # Prüfen, ob URL angegeben wurde
    if not args.url:
        logger.error("Keine YouTube-URL angegeben")
        print("Fehler: Bitte geben Sie eine YouTube-URL mit --url an.")
        sys.exit(1)
    
    try:
        # Temporäre und Ausgabeverzeichnisse erstellen
        temp_dir = Path(config["paths"]["temp_download"])
        output_dir = Path(args.output if args.output else config["paths"]["output"])
        
        temp_dir.mkdir(exist_ok=True)
        output_dir.mkdir(exist_ok=True)
        
        # YouTube-Video herunterladen
        downloader = YouTubeDownloader(config)
        video_path, video_info = downloader.download_video(args.url, temp_dir)
        
        # Zu MP3 konvertieren
        converter = AudioConverter(config)
        mp3_path = converter.convert_to_mp3(video_path, output_dir)
        
        # Aufräumen
        downloader.cleanup(video_path)
        
        print(f"Video erfolgreich heruntergeladen und zu MP3 konvertiert: {mp3_path}")
        
        # Auf USB-Stick kopieren, wenn gewünscht
        if args.usb:
            usb_handler = USBHandler(config)
            usb_drive = usb_handler.detect_usb_drive()
            
            if usb_drive:
                usb_handler.copy_to_usb(mp3_path, usb_drive)
                print(f"MP3-Datei erfolgreich auf USB-Stick {usb_drive} kopiert")
            else:
                logger.warning("Kein USB-Stick gefunden")
                print("Warnung: Kein USB-Stick gefunden")
        
        logger.info("Programm erfolgreich beendet")
        
    except Exception as e:
        logger.exception("Ein Fehler ist aufgetreten")
        print(f"Fehler: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()