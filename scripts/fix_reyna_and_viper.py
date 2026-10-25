import os, sys, json, subprocess
import imageio_ffmpeg

sys.stdout.reconfigure(encoding='utf-8')
ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()

BASE_DIR = 'D:/code-projects/valorant-replik'
AUDIO_DIR = os.path.join(BASE_DIR, 'audio')
DATA_PATH = os.path.join(BASE_DIR, 'data/quotes.json')

# 1. Update pure_quote_11.mp3 with Reyna's ingame_223.mp3
src_11 = os.path.join(AUDIO_DIR, 'ingame_223.mp3')
dest_11 = os.path.join(AUDIO_DIR, 'pure_quote_11.mp3')
subprocess.run([ffmpeg, '-i', src_11, '-vn', '-c:a', 'libmp3lame', '-q:a', '2', dest_11, '-y'], capture_output=True)
print("Updated pure_quote_11.mp3 with Reyna voice line!")

# 2. Update pure_quote_40.mp3 with Viper's ingame_226.mp3
src_40 = os.path.join(AUDIO_DIR, 'ingame_226.mp3')
dest_40 = os.path.join(AUDIO_DIR, 'pure_quote_40.mp3')
subprocess.run([ffmpeg, '-i', src_40, '-vn', '-c:a', 'libmp3lame', '-q:a', '2', dest_40, '-y'], capture_output=True)
print("Updated pure_quote_40.mp3 with Viper voice line!")

# 3. Create pure_quote_49_reyna.mp3 from ingame_249.mp3
src_49 = os.path.join(AUDIO_DIR, 'ingame_249.mp3')
dest_49 = os.path.join(AUDIO_DIR, 'pure_quote_49_reyna.mp3')
subprocess.run([ffmpeg, '-i', src_49, '-vn', '-c:a', 'libmp3lame', '-q:a', '2', dest_49, '-y'], capture_output=True)
print("Created pure_quote_49_reyna.mp3 with Reyna soul-hunger line!")

# 4. Load and update quotes.json
quotes = json.load(open(DATA_PATH, encoding='utf-8'))

for q in quotes:
    # Fix quote_10: Viper says "Bana canavar diyorlar..."
    if q['id'] == 'quote_10':
        q['agent'] = 'Viper'
        q['category'] = 'Tur Başı / Viper'
        print(f"Fixed quote_10: set agent to Viper ('{q['quote']}')")
    
    # Fix quote_11: Reyna says "Karşımızdakilerin bir özelliği yok..."
    elif q['id'] == 'quote_11':
        q['agent'] = 'Reyna'
        q['quote'] = 'Karşımızdakilerin bir özelliği yok. Yine insan, yine ölümlü.'
        q['category'] = 'Tur Başı / Reyna'
        print(f"Fixed quote_11: set agent to Reyna ('{q['quote']}')")

    # Fix quote_38: Viper says "Breach, lütfen şunların içini açar mısın..."
    elif q['id'] == 'quote_38':
        q['agent'] = 'Viper'
        q['quote'] = 'Breach, lütfen şunların içini açar mısın? Zehirler en iyi doğrudan enjekte edince işe yarıyor.'
        q['category'] = 'Ajan Etkileşimi / Viper'
        print(f"Fixed quote_38: set agent to Viper ('{q['quote']}')")

# Add Reyna quote_49 if not already present
if not any(q['id'] == 'quote_49' for q in quotes):
    quotes.append({
        "id": "quote_49",
        "agent": "Reyna",
        "quote": "Hepsi gitti ama ben doymadım!",
        "category": "Katletme / Reyna",
        "audioUrl": "audio/pure_quote_49_reyna.mp3"
    })
    print("Added quote_49: Reyna ('Hepsi gitti ama ben doymadım!')")

with open(DATA_PATH, 'w', encoding='utf-8') as f:
    json.dump(quotes, f, ensure_ascii=False, indent=2)

print("\nSuccessfully updated quotes.json! Total quotes:", len(quotes))
