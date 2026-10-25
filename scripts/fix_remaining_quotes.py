import json, os, sys, subprocess
import imageio_ffmpeg

sys.stdout.reconfigure(encoding='utf-8')
ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()

DATA_PATH = "D:/code-projects/valorant-replik/data/quotes.json"
quotes = json.load(open(DATA_PATH, encoding='utf-8'))

# Exact fixes
for q in quotes:
    # 1. quote_28: Sova says this to Omen
    if "Kim olduğunu unutma Omen" in q['quote']:
        q['agent'] = 'Sova'
        q['category'] = 'Ajan Etkileşimi / Sova'
        print(f"Fixed {q['id']}: set agent to Sova")

    # 2. quote_32: Iso says this line
    elif "Baskıyı doğru uygularsan" in q['quote']:
        q['agent'] = 'Iso'
        q['category'] = 'Taktik / Iso'
        print(f"Fixed {q['id']}: set agent to Iso")

    # 3. quote_37: Reyna says this about Radiants
    elif "Teknolojiniz bitiyor" in q['quote']:
        q['agent'] = 'Reyna'
        q['category'] = 'Meydan Okuma / Reyna'
        print(f"Fixed {q['id']}: set agent to Reyna")

    # 4. quote_16: Replace with Chamber's authentic line
    elif "Brimstone, hadi yakalım şunları" in q['quote']:
        q['agent'] = 'Chamber'
        q['quote'] = 'Ben sana dedim, daha iyisini hak ediyorsun Viper. Biraz aç kalbini...'
        q['category'] = 'Ajan Etkileşimi / Chamber'
        # copy ingame_173.mp3 to quote's audio
        src = "D:/code-projects/valorant-replik/audio/ingame_173.mp3"
        dest = f"D:/code-projects/valorant-replik/{q['audioUrl']}"
        subprocess.run([ffmpeg, '-i', src, '-vn', '-c:a', 'libmp3lame', '-q:a', '2', dest, '-y'], capture_output=True)
        print(f"Fixed {q['id']}: updated to Chamber")

    # 5. quote_41: Replace with Viper's authentic acid line
    elif "Spike'ı alın ve yerlerinize" in q['quote']:
        q['agent'] = 'Viper'
        q['quote'] = 'Bir beden asitte 12 saat içinde çözünür. Bunu nereden mi biliyorum? Sormayın.'
        q['category'] = 'Karanlık / Viper'
        src = "D:/code-projects/valorant-replik/audio/ingame_150.mp3"
        dest = f"D:/code-projects/valorant-replik/{q['audioUrl']}"
        subprocess.run([ffmpeg, '-i', src, '-vn', '-c:a', 'libmp3lame', '-q:a', '2', dest, '-y'], capture_output=True)
        print(f"Fixed {q['id']}: updated to Viper (Acid line)")

    # 6. quote_45: Sova's hunter line
    elif "Kısa ve acıklı bir hayat" in q['quote']:
        q['agent'] = 'Cypher'
        q['category'] = 'Katletme / Cypher'
        print(f"Fixed {q['id']}: updated category to Cypher")

with open(DATA_PATH, 'w', encoding='utf-8') as f:
    json.dump(quotes, f, ensure_ascii=False, indent=2)

print("\nSaved updated quotes.json!")
