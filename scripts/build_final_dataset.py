import os, sys, json, shutil, subprocess
import imageio_ffmpeg
import speech_recognition as sr

sys.stdout.reconfigure(encoding='utf-8')
ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()

BASE_DIR = 'D:/code-projects/valorant-replik'
AUDIO_DIR = os.path.join(BASE_DIR, 'audio')
DATA_DIR = os.path.join(BASE_DIR, 'data')

# 50 100% Authentic Turkish localized in-game quotes directly from the pak file
quotes_data = [
    {
        "agent": "Jett",
        "quote": "Karşıda da mı Jett varmış? Yok be bir Jett var, o da bizde! Onlarınki anca çakma!",
        "category": "Maç Başı / Karşılaşma",
        "src": "ingame_65.mp3"
    },
    {
        "agent": "Sage",
        "quote": "Tüm gücümle hepinizi canım pahasına koruyacağım!",
        "category": "Tur Başı / Moral",
        "src": "ingame_79.mp3"
    },
    {
        "agent": "Sage",
        "quote": "Henüz ölemem, yapacaklarım var!",
        "category": "Can Azalma",
        "src": "ingame_5.mp3"
    },
    {
        "agent": "Phoenix",
        "quote": "Susayan var mı ya da terleyen bir sorayım?",
        "category": "Tur Başı / Şaka",
        "src": "ingame_3.mp3"
    },
    {
        "agent": "Phoenix",
        "quote": "Biz bu işi gözümüz kapalı yaparız da, siz yine de açık tutun!",
        "category": "Tur Başı",
        "src": "ingame_35.mp3"
    },
    {
        "agent": "Phoenix",
        "quote": "Benim kopyam o, bana bırak!",
        "category": "Ajan Etkileşimi",
        "src": "ingame_70.mp3"
    },
    {
        "agent": "Reyna",
        "quote": "Bana canavar diyorlar, onları haklı çıkarayım!",
        "category": "Tur Başı",
        "src": "ingame_24.mp3"
    },
    {
        "agent": "Reyna",
        "quote": "Kafalarından mı vursam, sırtlarından mı bıçaklasam? Neyse, sonra karar veririm.",
        "category": "Tur Başı / Taktik",
        "src": "ingame_18.mp3"
    },
    {
        "agent": "Omen",
        "quote": "Zamanım sonsuz, acelem yok.",
        "category": "Tur Başı",
        "src": "ingame_69.mp3"
    },
    {
        "agent": "Sova",
        "quote": "Sova, vakit av vakti!",
        "category": "Karakter Seçim",
        "src": "ingame_0.mp3"
    },
    {
        "agent": "Sova",
        "quote": "Sen onları bul, ben işlerini bitiririm.",
        "category": "Takım Etkileşimi",
        "src": "ingame_28.mp3"
    },
    {
        "agent": "Raze",
        "quote": "Müzik dinlemeyecek miyiz yani? Moralimi alt üst ettin be ciğerim!",
        "category": "Tur Başı / Müzik",
        "src": "ingame_76.mp3"
    },
    {
        "agent": "Raze",
        "quote": "Spike'ı almadım ama siz de almadınız, suç bende değil yani!",
        "category": "Spike Unutma",
        "src": "ingame_17.mp3"
    },
    {
        "agent": "Killjoy",
        "quote": "Not aldınız mı, tekrar göstereyim mi?",
        "category": "Tur Başı / Taktik",
        "src": "ingame_72.mp3"
    },
    {
        "agent": "Gekko",
        "quote": "Killjoy'un ayakkabılarını mı istiyorsun oğlum? Senin ayağına olmaz onlar!",
        "category": "Kankuş Etkileşimi",
        "src": "ingame_27.mp3"
    },
    {
        "agent": "Viper",
        "quote": "Canımı yaksa da burası benim dünyam ve onun için can alırım!",
        "category": "Tur Başı",
        "src": "ingame_4.mp3"
    },
    {
        "agent": "Neon",
        "quote": "Çekil yoldan, çarpılırsın!",
        "category": "Yetenek / Hız",
        "src": "ingame_73.mp3"
    },
    {
        "agent": "Harbor",
        "quote": "Astra, eldivenin altı kaşınınca ne yapıyorsun? Şu bileklik beni delirtmek üzere!",
        "category": "Ajan Etkileşimi",
        "src": "ingame_6.mp3"
    },
    {
        "agent": "Fade",
        "quote": "Sova, kendine dikkat et. Bizim için bir gözünü feda ettin zaten, diğeri kalsın.",
        "category": "Ajan Etkileşimi",
        "src": "ingame_22.mp3"
    },
    {
        "agent": "Brimstone",
        "quote": "Vakit geldi. Rolünüzü unutmayın, sinirlerinize hakim olun. Beceremezseniz ben hallederim!",
        "category": "Komutan Emri",
        "src": "ingame_36.mp3"
    },
    {
        "agent": "Brimstone",
        "quote": "Ekip çalışması yapıyoruz tamam mı? Kimse kahramanlık yapmaya kalkıp işi batırmasın.",
        "category": "Tur Başı",
        "src": "ingame_42.mp3"
    },
    {
        "agent": "Skye",
        "quote": "Doğru ellerde her şey bir silah olabilir ama ağaçlarla kimseyi öldürdüğümü hatırlamıyorum.",
        "category": "Tur Başı",
        "src": "ingame_9.mp3"
    },
    {
        "agent": "Neon",
        "quote": "Pekala millet, bugün enerjimiz yerinde. Yoru'yu da gülümsettik, değmeyin keyfime!",
        "category": "Tur Kazanma",
        "src": "ingame_74.mp3"
    },
    {
        "agent": "KAY/O",
        "quote": "Tarihi geçmiş askerler...",
        "category": "Katletme",
        "src": "ingame_75.mp3"
    },
    {
        "agent": "Cypher",
        "quote": "Özür dilerim, sorarlarsa kahramanca öldüler derim.",
        "category": "Katletme",
        "src": "ingame_45.mp3"
    },
    {
        "agent": "Astra",
        "quote": "Tabii ki, sadece bir arkadaşıma yardım etmek istiyorum o kadar!",
        "category": "Ajan Etkileşimi",
        "src": "ingame_80.mp3"
    },
    {
        "agent": "Iso",
        "quote": "Zaferi bizden ayıran bu son savaş!",
        "category": "Maç Sayısı / Tur Başı",
        "src": "ingame_81.mp3"
    },
    {
        "agent": "Jett",
        "quote": "Rüzgar güçlü, önümüz açık. Hadi yap şovunu!",
        "category": "Tur Başı",
        "src": "ingame_83.mp3"
    },
    {
        "agent": "Cypher",
        "quote": "Kubbenin ötesindeki şu kale milattan önce 48 civarında yapılmış. Kurtarılamadı, yazık olmuş.",
        "category": "Harita İnceleme",
        "src": "ingame_84.mp3"
    },
    {
        "agent": "Fade",
        "quote": "Bize mi saldıracaklar? Tabutuna çivi lazım herhalde.",
        "category": "Meydan Okuma",
        "src": "ingame_85.mp3"
    },
    {
        "agent": "Brimstone",
        "quote": "Suyunuzu için, şarjörleri doldurun, doğru iş başına!",
        "category": "Tur Başı / Hazırlık",
        "src": "ingame_86.mp3"
    },
    {
        "agent": "Jett",
        "quote": "Başka figürler çağırmayı denedin mi Skye? Aslan falan... Oha, ejderha çağırsana!",
        "category": "Ajan Etkileşimi",
        "src": "ingame_89.mp3"
    },
    {
        "agent": "Phoenix",
        "quote": "Söylesene, şu ölümsüzlük işi nasıl oldu?",
        "category": "Ajan Etkileşimi",
        "src": "ingame_90.mp3"
    },
    {
        "agent": "Reyna",
        "quote": "Affet beni anne, bugün can alacağım...",
        "category": "Tur Başı / Karanlık",
        "src": "ingame_94.mp3"
    },
    {
        "agent": "Sage",
        "quote": "Seni işini yaparken izlemek hiç sıkmıyor.",
        "category": "Övgü / Tur Sonu",
        "src": "ingame_96.mp3"
    },
    {
        "agent": "Fade",
        "quote": "Buraya barış için gelmediler, siz de insafa gelmeyin!",
        "category": "Tur Başı / Uyarı",
        "src": "ingame_103.mp3"
    },
    {
        "agent": "Omen",
        "quote": "Şirketin sadık adamı Brimstone, buraya ayak işlerini görmeye mi geldin?",
        "category": "Ajan Etkileşimi",
        "src": "ingame_107.mp3"
    },
    {
        "agent": "Jett",
        "quote": "Gotik kız kabus gücü elde edince olan bu!",
        "category": "Ajan Etkileşimi",
        "src": "ingame_110.mp3"
    },
    {
        "agent": "Killjoy",
        "quote": "Dahi diye yazılır, dahi diye okunur!",
        "category": "Ego / Tur Başı",
        "src": "ingame_111.mp3"
    },
    {
        "agent": "Sova",
        "quote": "Kendine güvenmen çok güzel ama Spike'ı almayı da unutma!",
        "category": "Spike Uyarısı",
        "src": "ingame_115.mp3"
    },
    {
        "agent": "Cypher",
        "quote": "Bizim oralarda israf pek sevilmez.",
        "category": "Katletme / Ekonomi",
        "src": "ingame_117.mp3"
    },
    {
        "agent": "Breach",
        "quote": "Kiminle olsa savaşırım, herkesle savaşırım!",
        "category": "Tur Başı / Meydan Okuma",
        "src": "ingame_118.mp3"
    },
    {
        "agent": "Raze",
        "quote": "Zamanı geldi, uçalım canım!",
        "category": "Tur Başı / Enerji",
        "src": "ingame_121.mp3"
    },
    {
        "agent": "Cypher",
        "quote": "İş bitiricilik 10 puan, gizlilik 0 puan!",
        "category": "Mizah / Tur Sonu",
        "src": "ingame_123.mp3"
    },
    {
        "agent": "Fade",
        "quote": "Baskıyı doğru uygularsan herkes kırılır.",
        "category": "Taktik",
        "src": "ingame_126.mp3"
    },
    {
        "agent": "Iso",
        "quote": "Clove, gecenin 3'ünde oturmuş yemek videoları izliyordum... Hayatta nasıl duruyorsun ki?!",
        "category": "Ajan Etkileşimi",
        "src": "ingame_131.mp3"
    },
    {
        "agent": "Cypher",
        "quote": "Taktikleri olsa analiz edeceğim ama yok!",
        "category": "Tur Sonu / Alay",
        "src": "ingame_133.mp3"
    },
    {
        "agent": "Killjoy",
        "quote": "Tek tuşla dünyayı kurtarıyoruz, zor iş değil!",
        "category": "Tur Başı / Teknoloji",
        "src": "ingame_134.mp3"
    },
    {
        "agent": "Chamber",
        "quote": "Reyna, duyduğuma göre çok güzel gitar çalıyormuşsun. Kaçmak yok, bir ara bize de çalarsın!",
        "category": "Ajan Etkileşimi",
        "src": "ingame_41.mp3"
    },
    {
        "agent": "Breach",
        "quote": "Buraya savaşmaya geldim, Chamber ne dolaplar çeviriyor?",
        "category": "Ajan Etkileşimi",
        "src": "ingame_55.mp3"
    }
]

print(f"Building clean 50 quotes dataset...")
final_quotes = []

for i, item in enumerate(quotes_data, start=1):
    src_file = os.path.join(AUDIO_DIR, item["src"])
    out_name = f"pure_quote_{i}.mp3"
    out_file = os.path.join(AUDIO_DIR, out_name)
    
    if not os.path.exists(src_file):
        print(f"WARNING: Source {src_file} does not exist!")
        continue
    
    # Re-encode cleanly so headers are pristine
    subprocess.run([ffmpeg, '-i', src_file, '-vn', '-c:a', 'libmp3lame', '-q:a', '2', out_file, '-y'], capture_output=True)
    
    final_quotes.append({
        "id": f"quote_{i}",
        "agent": item["agent"],
        "quote": item["quote"],
        "category": item["category"],
        "audioUrl": f"audio/{out_name}"
    })
    print(f"[{i:02d}/50] ({item['agent']}) -> {out_name} : \"{item['quote'][:45]}...\"")

quotes_json_path = os.path.join(DATA_DIR, 'quotes.json')
with open(quotes_json_path, 'w', encoding='utf-8') as f:
    json.dump(final_quotes, f, ensure_ascii=False, indent=2)

print(f"\nSuccessfully wrote {len(final_quotes)} pure in-game quotes to {quotes_json_path}!")
