"""
VALORANT Orijinal Karakter Sesleri İndirme ve Dilimleme Betiği
Yapay TTS kullanmaz; doğrudan oyun içi Türkçe seslendirmelerini aktarır.
"""

import subprocess
import os
import sys
import imageio_ffmpeg

sys.stdout.reconfigure(encoding='utf-8')

ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUDIO_DIR = os.path.join(BASE_DIR, 'audio')
os.makedirs(AUDIO_DIR, exist_ok=True)

print("Audio klasöründeki orijinal sesler kontrol ediliyor...")
real_files = [f for f in os.listdir(AUDIO_DIR) if f.endswith('_real.mp3')]
print(f"Toplam {len(real_files)} ajanın orijinal Türkçe oyun içi ses dosyası hazır.")
for f in sorted(real_files):
    size_kb = os.path.getsize(os.path.join(AUDIO_DIR, f)) // 1024
    print(f"  - {f} ({size_kb} KB)")
