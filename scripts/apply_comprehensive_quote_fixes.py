import os, sys, json, subprocess
import imageio_ffmpeg

sys.stdout.reconfigure(encoding='utf-8')
ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()

BASE_DIR = 'D:/code-projects/valorant-replik'
AUDIO_DIR = os.path.join(BASE_DIR, 'audio')
DATA_PATH = os.path.join(BASE_DIR, 'data/quotes.json')

quotes = json.load(open(DATA_PATH, encoding='utf-8'))

# 1. Update pure_quote_3.mp3 with Jett's ingame_219.mp3
src_jett = os.path.join(AUDIO_DIR, 'ingame_219.mp3')
dest_jett = os.path.join(AUDIO_DIR, 'pure_quote_3.mp3')
subprocess.run([ffmpeg, '-i', src_jett, '-vn', '-c:a', 'libmp3lame', '-q:a', '2', dest_jett, '-y'], capture_output=True)
print("Updated pure_quote_3.mp3 with Jett's hair gel line to Yoru!")

# 2. Update pure_quote_23.mp3 with Cypher's ingame_304.mp3
src_cypher = os.path.join(AUDIO_DIR, 'ingame_304.mp3')
dest_cypher = os.path.join(AUDIO_DIR, 'pure_quote_23.mp3')
subprocess.run([ffmpeg, '-i', src_cypher, '-vn', '-c:a', 'libmp3lame', '-q:a', '2', dest_cypher, '-y'], capture_output=True)
print("Updated pure_quote_23.mp3 with Cypher's family lore line!")

# 3. Update pure_quote_50.mp3 with Skye's ingame_280.mp3
src_skye = os.path.join(AUDIO_DIR, 'ingame_280.mp3')
dest_skye = os.path.join(AUDIO_DIR, 'pure_quote_50.mp3')
subprocess.run([ffmpeg, '-i', src_skye, '-vn', '-c:a', 'libmp3lame', '-q:a', '2', dest_skye, '-y'], capture_output=True)
print("Updated pure_quote_50.mp3 with Skye's doctor line!")

# 4. Create pure_quote_50_gekko.mp3 from ingame_220.mp3
src_gekko = os.path.join(AUDIO_DIR, 'ingame_220.mp3')
dest_gekko = os.path.join(AUDIO_DIR, 'pure_quote_50_gekko.mp3')
subprocess.run([ffmpeg, '-i', src_gekko, '-vn', '-c:a', 'libmp3lame', '-q:a', '2', dest_gekko, '-y'], capture_output=True)
print("Created pure_quote_50_gekko.mp3 with Gekko's ponçikler line!")

# Apply updates to quotes in JSON
for q in quotes:
    # Fix quote_3: Jett hair gel line
    if q['id'] == 'quote_3':
        q['agent'] = 'Jett'
        q['quote'] = 'Saçına sürdüğün şeyden biraz da bana ver! Sağa sola uçup duruyorum, saçlarım perişan...'
        q['category'] = 'Ajan Etkileşimi / Jett'
        print(f"Fixed quote_3: Jett hair gel line")

    # Fix quote_22: Cypher family lore
    elif q['id'] == 'quote_22':
        q['agent'] = 'Cypher'
        q['quote'] = 'Ailemi korumak için hayatta kalmalıyım, onları kaybedemem o acıyı tekrar yaşayamam.'
        q['category'] = 'Hikaye / Cypher'
        print(f"Fixed quote_22: Cypher family lore")

    # Fix quote_23: Harbor says the 48 BC Pearl line, not Cypher!
    elif q['id'] == 'quote_23':
        q['agent'] = 'Harbor'
        q['category'] = 'Harita İnceleme / Harbor'
        print(f"Fixed quote_23: Changed agent to Harbor (Pearl 48 BC line)")

    # Fix quote_46: Skye doctor line
    elif q['id'] == 'quote_46':
        q['agent'] = 'Skye'
        q['quote'] = 'Doktor değilim ama bir iki kurşun yarasını halledebilirim. Şifa lazımsa haber ver!'
        q['category'] = 'Şifa / Skye'
        print(f"Fixed quote_46: Skye doctor healing line")

    # Fix quote_47: Astra typo
    elif q['id'] == 'quote_47':
        q['quote'] = 'Düzlemim sahiden yukarıda çiçeğim, lafta değil.'
        print(f"Fixed quote_47: Astra typo (Düzlemim)")

# Add Gekko quote_50 if not exists
if not any(q['id'] == 'quote_50' for q in quotes):
    quotes.append({
        "id": "quote_50",
        "agent": "Gekko",
        "quote": "Sıkmayın canınızı ponçikler, daha bitmedi!",
        "category": "Moral / Gekko",
        "audioUrl": "audio/pure_quote_50_gekko.mp3"
    })
    print("Added quote_50: Gekko (ponçikler line)")

with open(DATA_PATH, 'w', encoding='utf-8') as f:
    json.dump(quotes, f, ensure_ascii=False, indent=2)

print("\nSuccessfully applied all comprehensive fixes! Total quotes:", len(quotes))
