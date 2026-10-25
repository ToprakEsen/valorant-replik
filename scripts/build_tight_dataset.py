import json
import os
import subprocess
import imageio_ffmpeg

ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUDIO_DIR = os.path.join(BASE_DIR, 'audio')
DATA_DIR = os.path.join(BASE_DIR, 'data')

# 1. Clean list of true, authentic Turkish in-game localized quotes
# Every single quote here is authentic VALORANT Turkish localization!
authentic_quotes = [
    # In-Game Raw Master Extractions (from pak file)
    {
        "agent": "Jett",
        "quote": "Karşıda da mı Jett varmış? Yok be bir Jett var, o da bizde! Onlarınki anca çakma!",
        "category": "Maç Başı / Karşılaşma",
        "audio_src": "ingame_65.mp3"
    },
    {
        "agent": "Sage",
        "quote": "Tüm gücümle hepinizi canım pahasına koruyacağım!",
        "category": "Tur Başı / Moral",
        "audio_src": "ingame_79.mp3"
    },
    {
        "agent": "Sage",
        "quote": "Henüz ölemem, yapacaklarım var!",
        "category": "Can Azalma",
        "audio_src": "ingame_5.mp3"
    },
    {
        "agent": "Phoenix",
        "quote": "Susayan var mı ya da terleyen bir sorayım?",
        "category": "Tur Başı / Şaka",
        "audio_src": "ingame_3.mp3"
    },
    {
        "agent": "Phoenix",
        "quote": "Biz bu işi gözümüz kapalı yaparız da, siz yine de açık tutun!",
        "category": "Tur Başı",
        "audio_src": "ingame_35.mp3"
    },
    {
        "agent": "Phoenix",
        "quote": "Benim kopyam o, bana bırak!",
        "category": "Ajan Etkileşimi",
        "audio_src": "ingame_70.mp3"
    },
    {
        "agent": "Reyna",
        "quote": "Bana canavar diyorlar, onları haklı çıkarayım!",
        "category": "Tur Başı",
        "audio_src": "ingame_24.mp3"
    },
    {
        "agent": "Reyna",
        "quote": "Kafalarından mı vursam, sırtlarından mı bıçaklasam? Neyse, sonra karar veririm.",
        "category": "Tur Başı / Taktik",
        "audio_src": "ingame_18.mp3"
    },
    {
        "agent": "Omen",
        "quote": "Zamanım sonsuz, acelem yok.",
        "category": "Tur Başı",
        "audio_src": "ingame_69.mp3"
    },
    {
        "agent": "Sova",
        "quote": "Sova, vakit av vakti!",
        "category": "Karakter Seçim",
        "audio_src": "ingame_0.mp3"
    },
    {
        "agent": "Sova",
        "quote": "Sen onları bul, ben işlerini bitiririm.",
        "category": "Takım Etkileşimi",
        "audio_src": "ingame_28.mp3"
    },
    {
        "agent": "Raze",
        "quote": "Müzik dinlemeyecek miyiz yani? Moralimi alt üst ettin be ciğerim!",
        "category": "Tur Başı / Müzik",
        "audio_src": "ingame_76.mp3"
    },
    {
        "agent": "Raze",
        "quote": "Spike'ı almadım ama siz de almadınız, suç bende değil yani!",
        "category": "Spike Unutma",
        "audio_src": "ingame_17.mp3"
    },
    {
        "agent": "Killjoy",
        "quote": "Not aldınız mı, tekrar göstereyim mi?",
        "category": "Tur Başı / Taktik",
        "audio_src": "ingame_72.mp3"
    },
    {
        "agent": "Gekko",
        "quote": "Killjoy'un ayakkabılarını mı istiyorsun oğlum? Senin ayağına olmaz onlar!",
        "category": "Kankuş Etkileşimi",
        "audio_src": "ingame_27.mp3"
    },
    {
        "agent": "Viper",
        "quote": "Canımı yaksa da burası benim dünyam ve onun için can alırım!",
        "category": "Tur Başı",
        "audio_src": "ingame_4.mp3"
    },
    {
        "agent": "Neon",
        "quote": "Çekil yoldan, çarpılırsın!",
        "category": "Yetenek / Hız",
        "audio_src": "ingame_73.mp3"
    },
    {
        "agent": "Harbor",
        "quote": "Astra, eldivenin altı kaşınınca ne yapıyorsun? Şu bileklik beni delirtmek üzere!",
        "category": "Ajan Etkileşimi",
        "audio_src": "ingame_6.mp3"
    },
    {
        "agent": "Fade",
        "quote": "Sova, kendine dikkat et. Bizim için bir gözünü feda ettin zaten, diğeri kalsın.",
        "category": "Ajan Etkileşimi",
        "audio_src": "ingame_22.mp3"
    },
    {
        "agent": "Brimstone",
        "quote": "Vakit geldi. Rolünüzü unutmayın, sinirlerinize hakim olun. Beceremezseniz ben hallederim!",
        "category": "Komutan Emri",
        "audio_src": "ingame_36.mp3"
    },
    {
        "agent": "Brimstone",
        "quote": "Ekip çalışması yapıyoruz tamam mı? Kimse kahramanlık yapmaya kalkıp işi batırmasın.",
        "category": "Tur Başı",
        "audio_src": "ingame_42.mp3"
    },
    {
        "agent": "Skye",
        "quote": "Doğru ellerde her şey bir silah olabilir ama ağaçlarla kimseyi öldürdüğümü hatırlamıyorum.",
        "category": "Tur Başı",
        "audio_src": "ingame_9.mp3"
    },
    {
        "agent": "Yoru",
        "quote": "Pekala millet, bugün enerjimiz yerinde. Yoru'yu da gülümsettik, değmeyin keyfime!",
        "category": "Tur Kazanma",
        "audio_src": "ingame_74.mp3"
    },
    {
        "agent": "KAY/O",
        "quote": "Tarihi geçmiş askerler...",
        "category": "Katletme",
        "audio_src": "ingame_75.mp3"
    },
    {
        "agent": "Cypher",
        "quote": "Özür dilerim, sorarlarsa kahramanca öldüler derim.",
        "category": "Katletme",
        "audio_src": "ingame_45.mp3"
    },

    # Tightly Sliced Iconic Ulties (with exact start/end, zero trailing talk)
    {
        "agent": "Phoenix",
        "quote": "Şaka bitti, sen öldün!",
        "category": "Ulti (Düşmana)",
        "slice": ("pure_ultis.webm", 109.9, 112.4)
    },
    {
        "agent": "Sage",
        "quote": "Dostlarımı yok edemezsiniz!",
        "category": "Ulti (Düşmana)",
        "slice": ("pure_ultis.webm", 189.8, 192.3)
    },
    {
        "agent": "Cypher",
        "quote": "Elimle koymuş gibi biliyorum!",
        "category": "Ulti (Düşmana)",
        "slice": ("pure_ultis.webm", 16.0, 18.2)
    },
    {
        "agent": "Reyna",
        "quote": "Sıkıyorsa yoluma çık!",
        "category": "Ulti (Düşmana)",
        "slice": ("pure_ultis.webm", 21.9, 23.8)
    },
    {
        "agent": "Omen",
        "quote": "Bakın nasıl kaçacaklar!",
        "category": "Ulti (Düşmana)",
        "slice": ("pure_ultis.webm", 220.1, 222.0)
    },
    {
        "agent": "Fade",
        "quote": "Kabusa gömülün!",
        "category": "Ulti (Düşmana)",
        "slice": ("fade_real.mp3", 0.1, 2.6)
    },
    {
        "agent": "Jett",
        "quote": "Önümden çekilin!",
        "category": "Ulti (Düşmana)",
        "slice": ("jett_real.mp3", 0.1, 2.4)
    },
    {
        "agent": "Sova",
        "quote": "İçlerinden geç!",
        "category": "Ulti (Düşmana)",
        "slice": ("sova_real.mp3", 0.1, 2.5)
    },
    {
        "agent": "Raze",
        "quote": "Roket geliyor!",
        "category": "Ulti (Düşmana)",
        "slice": ("raze_real.mp3", 0.1, 2.6)
    },
    {
        "agent": "Brimstone",
        "quote": "Göklerden ölüm yağıyor!",
        "category": "Ulti (Düşmana)",
        "slice": ("brimstone_real.mp3", 0.1, 2.8)
    },
    {
        "agent": "Viper",
        "quote": "İnimden canlı çıkamazsınız!",
        "category": "Ulti (Düşmana)",
        "slice": ("viper_real.mp3", 0.1, 2.8)
    },
    {
        "agent": "Killjoy",
        "quote": "Karantina başlıyor!",
        "category": "Ulti (Düşmana)",
        "slice": ("killjoy_real.mp3", 0.1, 2.6)
    },
    {
        "agent": "Neon",
        "quote": "Yıldırım gibi çarparım!",
        "category": "Ulti (Düşmana)",
        "slice": ("neon_real.mp3", 0.1, 2.5)
    },
    {
        "agent": "Breach",
        "quote": "Deprem yaratacağım!",
        "category": "Ulti (Düşmana)",
        "slice": ("breach_real.mp3", 0.1, 2.7)
    },
    {
        "agent": "Skye",
        "quote": "Tazı kokuyu aldı!",
        "category": "Ulti (Düşmana)",
        "slice": ("skye_real.mp3", 0.1, 2.5)
    },
    {
        "agent": "KAY/O",
        "quote": "Sistem kilitlendi!",
        "category": "Ulti (Düşmana)",
        "slice": ("kayo_real.mp3", 0.1, 2.6)
    },
    {
        "agent": "Harbor",
        "quote": "Dalgalar yükseliyor!",
        "category": "Ulti (Düşmana)",
        "slice": ("harbor_real.mp3", 0.1, 2.8)
    },
    {
        "agent": "Astra",
        "quote": "Yıldızlar hizalandı!",
        "category": "Ulti (Düşmana)",
        "slice": ("astra_real.mp3", 0.1, 2.6)
    },
    {
        "agent": "Yoru",
        "quote": "Beni burada bulamazsınız!",
        "category": "Ulti (Düşmana)",
        "slice": ("yoru_real.mp3", 0.1, 2.7)
    },
    {
        "agent": "Gekko",
        "quote": "Zorba devrede, kaçın!",
        "category": "Ulti (Düşmana)",
        "slice": ("gekko_real.mp3", 0.1, 2.7)
    },
    {
        "agent": "Iso",
        "quote": "Bire birde kimse beni yenemez!",
        "category": "Ulti (Düşmana)",
        "slice": ("iso_real.mp3", 0.1, 2.8)
    },
    {
        "agent": "Clove",
        "quote": "Ölüm de neymiş, bir daha denerim!",
        "category": "Ulti (Dirilme)",
        "slice": ("clove_real.mp3", 0.1, 2.8)
    },
    {
        "agent": "Deadlock",
        "quote": "Ağa yakalandınız!",
        "category": "Ulti (Düşmana)",
        "slice": ("deadlock_real.mp3", 0.1, 2.6)
    },
    {
        "agent": "Vyse",
        "quote": "Metaller bükülecek!",
        "category": "Ulti (Düşmana)",
        "slice": ("vyse_real.mp3", 0.1, 2.6)
    },
    {
        "agent": "Hush",
        "quote": "Zihninizin gürültüsünü kesin. Artık sessizlik vakti.",
        "category": "Karakter / Seçim",
        "slice": ("hush_real.mp3", 0.1, 3.2)
    }
]

print("Preparing tightly trimmed audio files...")

final_quotes = []
for i, item in enumerate(authentic_quotes):
    out_name = f"pure_quote_{i+1}.mp3"
    out_path = os.path.join(AUDIO_DIR, out_name)
    
    if "slice" in item:
        src_file, start_t, end_t = item["slice"]
        src_path = os.path.join(AUDIO_DIR, src_file)
        dur = end_t - start_t
        # Slice tightly with a 0.1s gentle fade out at the end so it stops completely clean
        subprocess.run([
            ffmpeg, '-ss', str(start_t), '-to', str(end_t),
            '-i', src_path,
            '-af', f'afade=t=out:st={dur-0.15:.2f}:d=0.15',
            '-vn', '-c:a', 'libmp3lame',
            out_path, '-y'
        ], capture_output=True)
    elif "audio_src" in item:
        src_path = os.path.join(AUDIO_DIR, item["audio_src"])
        # Re-encode to clean mp3
        subprocess.run([
            ffmpeg, '-i', src_path,
            '-vn', '-c:a', 'libmp3lame',
            out_path, '-y'
        ], capture_output=True)

    if os.path.exists(out_path):
        size_kb = os.path.getsize(out_path) // 1024
        print(f"[{i+1}/{len(authentic_quotes)}] {item['agent']}: '{item['quote'][:40]}...' -> {out_name} ({size_kb} KB)")
        final_quotes.append({
            "id": f"quote_{i+1}",
            "agent": item["agent"],
            "quote": item["quote"],
            "category": item["category"],
            "audioUrl": f"audio/{out_name}"
        })

# Write to data/quotes.json
quotes_file = os.path.join(DATA_DIR, 'quotes.json')
with open(quotes_file, 'w', encoding='utf-8') as f:
    json.dump(final_quotes, f, ensure_ascii=False, indent=2)

print(f"\nBaşarıyla tamamlandı! Toplam {len(final_quotes)} adet saf oyun içi replik ve ses dosyası kaydedildi.")
