import subprocess
import os
import sys
import imageio_ffmpeg

sys.stdout.reconfigure(encoding='utf-8')

ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
AUDIO_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'audio')

new_agents = {
    "gekko": "eH9RJtFksFU",
    "deadlock": "JIsvYGfT_V8",
    "iso": "2nxicJmC-TQ",
    "vyse": "TSw0Iom1VFk",
    "hush": "Xcfq-_LyG2A"
}

for agent, vid in new_agents.items():
    out_mp3 = os.path.join(AUDIO_DIR, f"{agent}_real.mp3")
    temp_webm = os.path.join(AUDIO_DIR, f"{agent}_temp.webm")
    print(f"Downloading {agent} ({vid})...")
    
    # Download audio format 251 or bestaudio
    dl_res = subprocess.run([
        'yt-dlp', f'https://www.youtube.com/watch?v={vid}',
        '-f', 'ba/251/140',
        '--max-filesize', '15M',
        '-o', temp_webm
    ], capture_output=True, text=True)
    
    if os.path.exists(temp_webm):
        # Convert first 8 seconds to mp3
        subprocess.run([
            ffmpeg, '-ss', '0', '-to', '8',
            '-i', temp_webm,
            '-vn', '-c:a', 'libmp3lame',
            out_mp3, '-y'
        ], capture_output=True)
        try:
            os.remove(temp_webm)
        except Exception:
            pass
        print(f"-> Created {agent}_real.mp3 ({os.path.getsize(out_mp3)} bytes)")
    else:
        print(f"Could not download {agent}: {dl_res.stderr[:200]}")

# For clove (from all_ultis.webm or fallback)
clove_mp3 = os.path.join(AUDIO_DIR, "clove_real.mp3")
if not os.path.exists(clove_mp3):
    # Slice from phoenix_real or sage_real as fallback or download
    subprocess.run([
        'yt-dlp', 'ytsearch1:valorant clove türkçe ulti repliği',
        '-f', 'ba/251',
        '-o', os.path.join(AUDIO_DIR, 'clove_temp.webm')
    ], capture_output=True)
    temp = os.path.join(AUDIO_DIR, 'clove_temp.webm')
    if os.path.exists(temp):
        subprocess.run([ffmpeg, '-ss', '0', '-to', '8', '-i', temp, '-vn', '-c:a', 'libmp3lame', clove_mp3, '-y'], capture_output=True)
        os.remove(temp)

print("Tamamlandı!")
