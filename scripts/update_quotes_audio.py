import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
AUDIO_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'audio')
quotes_path = os.path.join(DATA_DIR, 'quotes.json')

with open(quotes_path, 'r', encoding='utf-8') as f:
    quotes = json.load(f)

# Mapping table
agent_audio_map = {
    "astra": "audio/astra_real.mp3",
    "breach": "audio/breach_real.mp3",
    "brimstone": "audio/brimstone_real.mp3",
    "chamber": "audio/chamber_real.mp3",
    "clove": "audio/clove_real.mp3",
    "cypher": "audio/cypher_real.mp3",
    "deadlock": "audio/deadlock_real.mp3",
    "fade": "audio/fade_real.mp3",
    "gekko": "audio/gekko_real.mp3",
    "harbor": "audio/harbor_real.mp3",
    "hush": "audio/hush_real.mp3",
    "iso": "audio/iso_real.mp3",
    "jett": "audio/jett_real.mp3",
    "kay/o": "audio/kayo_real.mp3",
    "kayo": "audio/kayo_real.mp3",
    "killjoy": "audio/killjoy_real.mp3",
    "neon": "audio/neon_real.mp3",
    "omen": "audio/omen_real.mp3",
    "phoenix": "audio/phoenix_real.mp3",
    "raze": "audio/raze_real.mp3",
    "reyna": "audio/reyna_real.mp3",
    "sage": "audio/sage_real.mp3",
    "skye": "audio/skye_real.mp3",
    "sova": "audio/sova_real.mp3",
    "tejo": "audio/tejo_real.mp3",
    "viper": "audio/viper_real.mp3",
    "vyse": "audio/vyse_real.mp3",
    "yoru": "audio/yoru_real.mp3"
}

mapped_count = 0
for q in quotes:
    agent_key = q['agent'].strip().lower()
    audio_path = agent_audio_map.get(agent_key)
    if audio_path:
        q['audioUrl'] = audio_path
        mapped_count += 1
    else:
        # Default or fallback
        q['audioUrl'] = f"audio/{agent_key.replace('/', '')}_real.mp3"

with open(quotes_path, 'w', encoding='utf-8') as f:
    json.dump(quotes, f, ensure_ascii=False, indent=2)

print(f"Toplam {len(quotes)} replikten {mapped_count} tanesi orijinal oyun seslerine bağlandı.")
