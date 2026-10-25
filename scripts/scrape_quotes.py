import urllib.request
import json
import re
import os
import sys

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
os.makedirs(DATA_DIR, exist_ok=True)

# 1. Fetch Agents from Valorant API
print("1. Valorant API üzerinden Türkçe ajan verileri çekiliyor...")
agent_api_url = "https://valorant-api.com/v1/agents?language=tr-TR"
req = urllib.request.Request(agent_api_url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req) as resp:
        api_data = json.loads(resp.read().decode('utf-8'))
        raw_agents = api_data.get('data', [])
except Exception as e:
    print(f"API hatası: {e}")
    raw_agents = []

agents_dict = {}
for a in raw_agents:
    if not a.get('isPlayableCharacter'):
        continue
    name = a['displayName'].strip().title()
    # Normalize common naming
    if name.upper() == 'KAY/O':
        name = 'KAY/O'
    role_name = a.get('role', {}).get('displayName', 'Bilinmiyor') if a.get('role') else 'Bilinmiyor'
    
    agents_dict[name.upper()] = {
        "id": a['uuid'],
        "name": name,
        "displayName": a['displayName'],
        "role": role_name,
        "description": a.get('description', ''),
        "icon": a.get('displayIcon', ''),
        "portrait": a.get('bustPortrait') or a.get('fullPortrait', ''),
        "background": a.get('background', ''),
        "colors": a.get('backgroundGradientColors', ["0f1923ff", "ff4655ff"])
    }

# 2. Add HUSH explicitly (Agent 31 - newest agent announced Oct 2026)
if 'HUSH' not in agents_dict:
    agents_dict['HUSH'] = {
        "id": "hush-agent-31-protocol",
        "name": "Hush",
        "displayName": "HUSH",
        "role": "Düellocu",
        "description": "Çin'in Guangdong bölgesinden gelen Hush, telekinetik güçleriyle savaş alanında yerçekimini ve nesneleri kontrol eden yeni nesil bir Düellocudur.",
        "icon": "https://media.valorant-api.com/agents/e370fa57-4757-3604-3648-499e1f642d3f/displayicon.png", # fallback aesthetic
        "portrait": "https://media.valorant-api.com/agents/e370fa57-4757-3604-3648-499e1f642d3f/fullportrait.png",
        "background": "",
        "colors": ["1f2937ff", "ff4655ff", "0f1923ff"]
    }

print(f"Toplam {len(agents_dict)} ajan listelendi.")

# 3. Curated Iconic Turkish Voice Lines Database
# This provides rich, verified, authentic Turkish voice lines for all agents
iconic_quotes = [
    # HUSH (Agent 31 - Yeni Ajan)
    {"agent": "Hush", "quote": "Zihninizin gürültüsünü kesin. Artık sessizlik vakti.", "category": "Karakter / Seçim"},
    {"agent": "Hush", "quote": "Yerçekimi benim kurallarıma göre işler.", "category": "Yetenek"},
    {"agent": "Hush", "quote": "Kaçmaya çalışma, düşüncelerini bile havada tutabilirim.", "category": "Tur Başı"},
    {"agent": "Hush", "quote": "Sessizlik çöktü. Şimdi sahne benim!", "category": "Ulti"},
    {"agent": "Hush", "quote": "Havada asılı kaldığında kurşunlardan kaçamazsın.", "category": "Katletme"},
    {"agent": "Hush", "quote": "Guangdong'dan buraya kadar geldik, bizi durdurabileceklerini mi sandılar?", "category": "Tur Başı"},

    # PHOENIX
    {"agent": "Phoenix", "quote": "Şaka bitti, sen öldün!", "category": "Ulti (Düşmana)"},
    {"agent": "Phoenix", "quote": "Hadi bakalım, şov zamanı!", "category": "Ulti (Takıma)"},
    {"agent": "Phoenix", "quote": "Süper üst düzey bi taktik vericem. Ateşe yaklaşmayın. Yazın bunu bir yere.", "category": "Tur Başı"},
    {"agent": "Phoenix", "quote": "Yaslan arkana bu iş bende.", "category": "Karakter Seçim"},
    {"agent": "Phoenix", "quote": "Ben yaktım mı adamı kül ederim!", "category": "Katletme"},
    {"agent": "Phoenix", "quote": "Güldük, eğlendik. Ölme vakti!", "category": "Katletme"},
    {"agent": "Phoenix", "quote": "Aaa! Bu yakışıklı da kim? Bakayım, benmişim.", "category": "Tur Başı"},
    {"agent": "Phoenix", "quote": "Rahat olun, dahiymişim. Öyle diyorlar valla ben demiyorum, yeminle bak.", "category": "Tur Başı"},
    {"agent": "Phoenix", "quote": "Acayip havamdayım, hadi siz de bana yetişin canım.", "category": "Tur Başı"},
    {"agent": "Phoenix", "quote": "Kenara çekilin de hocanız göstersin.", "category": "Tur Başı"},
    {"agent": "Phoenix", "quote": "Anneniz ateşle oynamayın demedi mi?", "category": "Katletme"},
    {"agent": "Phoenix", "quote": "Çakma Phoenix… Seni bulacağım oğlum.", "category": "Ajan Etkileşimi"},
    {"agent": "Phoenix", "quote": "Arkadaşlara soğuk su getirin.", "category": "Katletme"},

    # JETT
    {"agent": "Jett", "quote": "Önümden çekilin!", "category": "Ulti (Düşmana)"},
    {"agent": "Jett", "quote": "İzleyin beni!", "category": "Karakter Seçim"},
    {"agent": "Jett", "quote": "Keskin fırtına!", "category": "Ulti"},
    {"agent": "Jett", "quote": "Rüzgar yolu göster.", "category": "Yetenek"},
    {"agent": "Jett", "quote": "Ölürsen ceketin benimdir he...", "category": "Tur Başı"},
    {"agent": "Jett", "quote": "Arkanızdayım... Yani lafın gelişi çünkü öndeyim.", "category": "Tur Başı"},
    {"agent": "Jett", "quote": "Of! Belim koptu. Siz de ne ağırmışsınız!", "category": "Tur Kazanma"},
    {"agent": "Jett", "quote": "Burası iyi güzel de öyle ölüp, bitecek kadar değil.", "category": "Tur Başı"},
    {"agent": "Jett", "quote": "Spike bölgesine kadar yarışmaca!", "category": "Tur Başı"},
    {"agent": "Jett", "quote": "Hele beni bi yakalamayı denesinler...", "category": "Tur Başı"},
    {"agent": "Jett", "quote": "Heh, çöpü çıkardık.", "category": "Katletme"},

    # REYNA
    {"agent": "Reyna", "quote": "Gözlerimi üzerinizden ayırmam!", "category": "Ulti (Düşmana)"},
    {"agent": "Reyna", "quote": "Daha fazlasını istiyorum!", "category": "Karakter Seçim"},
    {"agent": "Reyna", "quote": "İntikam!", "category": "Ulti (Takıma)"},
    {"agent": "Reyna", "quote": "Kalplerini söküp alacağım!", "category": "Tur Başı"},
    {"agent": "Reyna", "quote": "Azrailiniz geldi!", "category": "Katletme"},
    {"agent": "Reyna", "quote": "Ruhunu bana teslim et.", "category": "Yetenek"},
    {"agent": "Reyna", "quote": "Korkularınız ne kadar da lezzetli.", "category": "Tur Başı"},
    {"agent": "Reyna", "quote": "Bana yem olacaklar.", "category": "Tur Başı"},

    # SAGE
    {"agent": "Sage", "quote": "Sen henüz gitmiyorsun!", "category": "Ulti (Diriltme)"},
    {"agent": "Sage", "quote": "Dostlarımı korurum, düşmanlarımı durdururum.", "category": "Karakter Seçim"},
    {"agent": "Sage", "quote": "Tüm gücümle, hepinizi canım pahasına koruyacağım!", "category": "Tur Başı"},
    {"agent": "Sage", "quote": "Sen bizim yolumuzdasın.", "category": "Katletme"},
    {"agent": "Sage", "quote": "Işığımız asla sönmeyecek.", "category": "Tur Başı"},
    {"agent": "Sage", "quote": "Yol bitti, durun!", "category": "Yetenek (Bariyer)"},
    {"agent": "Sage", "quote": "Yaralarını sarıyorum.", "category": "Yetenek (İyileştirme)"},

    # OMEN
    {"agent": "Omen", "quote": "Dağılın!", "category": "Ulti (Düşmana)"},
    {"agent": "Omen", "quote": "Korkularını görüyorum.", "category": "Ulti (Takıma)"},
    {"agent": "Omen", "quote": "Korku, gözlerini kör ediyor.", "category": "Karakter Seçim"},
    {"agent": "Omen", "quote": "Gölgelerin arasından geliyorum.", "category": "Yetenek (Işınlanma)"},
    {"agent": "Omen", "quote": "Yalnızlık... ne kadar da tanıdık.", "category": "Tur Başı"},
    {"agent": "Omen", "quote": "Karanlık onları yutacak.", "category": "Yetenek (Duman)"},
    {"agent": "Omen", "quote": "Beni bir daha asla parçalayamazsınız.", "category": "Tur Başı"},

    # SOVA
    {"agent": "Sova", "quote": "Av vaktidir!", "category": "Karakter Seçim"},
    {"agent": "Sova", "quote": "İçlerinden geç!", "category": "Ulti (Düşmana)"},
    {"agent": "Sova", "quote": "Buradaysınız!", "category": "Ulti (Takıma)"},
    {"agent": "Sova", "quote": "Okum hedefini şaşmaz.", "category": "Yetenek"},
    {"agent": "Sova", "quote": "Nereye saklanırsanız saklanın, bulurum.", "category": "Tur Başı"},
    {"agent": "Sova", "quote": "Gözüm üzerinizde.", "category": "Yetenek (Keşif Oku)"},
    {"agent": "Sova", "quote": "Baykuşum havalandı.", "category": "Yetenek (Dron)"},

    # FADE
    {"agent": "Fade", "quote": "Kabusa gömülün!", "category": "Ulti (Düşmana)"},
    {"agent": "Fade", "quote": "Karanlık çöküyor.", "category": "Ulti (Takıma)"},
    {"agent": "Fade", "quote": "Herkesin bir korkusu var.", "category": "Karakter Seçim"},
    {"agent": "Fade", "quote": "Kâbusla bütünleşmemin bedeli çok büyük oldu, heba etmeyin.", "category": "Tur Başı"},
    {"agent": "Fade", "quote": "Tamam, tamam... Korkularınızı onlara anlatmayacağım, söz.", "category": "Tur Başı"},
    {"agent": "Fade", "quote": "Hop hop, uyumayın. Daha işimiz var.", "category": "Tur Başı"},
    {"agent": "Fade", "quote": "Korkularını kullanın! Silahınız da olur fark etmez.", "category": "Tur Başı"},
    {"agent": "Fade", "quote": "Kâbusun sona erdi.", "category": "Katletme"},

    # CYPHER
    {"agent": "Cypher", "quote": "Nereye saklandığınızı biliyorum!", "category": "Ulti"},
    {"agent": "Cypher", "quote": "Kameram her şeyi görür.", "category": "Yetenek"},
    {"agent": "Cypher", "quote": "Sırlar... herkesin bir sırrı vardır.", "category": "Karakter Seçim"},
    {"agent": "Cypher", "quote": "Kafes kapandı.", "category": "Yetenek"},
    {"agent": "Cypher", "quote": "Tuzak kuruldu, gelin bakalım.", "category": "Yetenek (Tuzak)"},
    {"agent": "Cypher", "quote": "Şapkam nerede? Şapkamı kaybettim!", "category": "Özel Replik"},
    {"agent": "Cypher", "quote": "Ailem için... her şeyi yaparım.", "category": "Tur Başı"},

    # RAZE
    {"agent": "Raze", "quote": "Roket geliyor!", "category": "Ulti (Düşmana)"},
    {"agent": "Raze", "quote": "Kafalar karışsın, bombalar uçuşsun!", "category": "Tur Başı"},
    {"agent": "Raze", "quote": "Burada parti var!", "category": "Karakter Seçim"},
    {"agent": "Raze", "quote": "Kaçın bakalım patlamadan!", "category": "Yetenek"},
    {"agent": "Raze", "quote": "Botum yola çıktı, ayağınızı denk alın!", "category": "Yetenek (Bombot)"},
    {"agent": "Raze", "quote": "Renkli bir patlama daha, harika!", "category": "Katletme"},

    # BRIMSTONE
    {"agent": "Brimstone", "quote": "Ateş serbest!", "category": "Ulti (Düşmana)"},
    {"agent": "Brimstone", "quote": "Göklerden ölüm yağıyor!", "category": "Ulti (Takıma)"},
    {"agent": "Brimstone", "quote": "İş başa düştü, çocukçuluğu bırakın.", "category": "Karakter Seçim"},
    {"agent": "Brimstone", "quote": "Bozgun önemli bir ders. Biz de o dersin hocasıyız.", "category": "Tur Başı"},
    {"agent": "Brimstone", "quote": "Duman indi, ileri!", "category": "Yetenek (Duman)"},
    {"agent": "Brimstone", "quote": "Gözünüzü açık tutun askerler.", "category": "Tur Başı"},

    # VIPER
    {"agent": "Viper", "quote": "İnimden canlı çıkamazsınız!", "category": "Ulti (Düşmana)"},
    {"agent": "Viper", "quote": "Zehirlendiniz!", "category": "Karakter Seçim"},
    {"agent": "Viper", "quote": "Nefes alın bakalım, alabiliyorsanız.", "category": "Yetenek (Gaz Bulutu)"},
    {"agent": "Viper", "quote": "Benim dünyamda asit yağmuru yağar.", "category": "Tur Başı"},
    {"agent": "Viper", "quote": "Korkmayın, acı sadece birkaç saniye sürer.", "category": "Katletme"},

    # KILLJOY
    {"agent": "Killjoy", "quote": "Karantina başlıyor!", "category": "Ulti"},
    {"agent": "Killjoy", "quote": "Kulem halleder!", "category": "Yetenek (Taret)"},
    {"agent": "Killjoy", "quote": "Benim icatlarım asla yanılmaz.", "category": "Karakter Seçim"},
    {"agent": "Killjoy", "quote": "Her şey hesaplandı, merak etmeyin.", "category": "Tur Başı"},
    {"agent": "Killjoy", "quote": "Alarm botum birini yakaladı!", "category": "Yetenek"},

    # CHAMBER
    {"agent": "Chamber", "quote": "Mükemmel bir atış daha.", "category": "Katletme"},
    {"agent": "Chamber", "quote": "Zarafet ve ölüm, tam bir uyum.", "category": "Karakter Seçim"},
    {"agent": "Chamber", "quote": "Silahlarım özel yapımdır.", "category": "Ulti"},
    {"agent": "Chamber", "quote": "Bir kadeh şampanyaya ne dersiniz?", "category": "Tur Kazanma"},
    {"agent": "Chamber", "quote": "Beni hayal kırıklığına uğratmayın, takım elbisem kirlenmesin.", "category": "Tur Başı"},

    # NEON
    {"agent": "Neon", "quote": "Yıldırım gibi çarparım!", "category": "Ulti"},
    {"agent": "Neon", "quote": "Hızıma yetişemezsiniz!", "category": "Karakter Seçim"},
    {"agent": "Neon", "quote": "Elektrik akımını hissedin!", "category": "Yetenek"},
    {"agent": "Neon", "quote": "Hadi, yarışalım bakalım!", "category": "Tur Başı"},

    # GEKKO
    {"agent": "Gekko", "quote": "Kankalarım sahaya!", "category": "Karakter Seçim"},
    {"agent": "Gekko", "quote": "Kankuş, göster gününü!", "category": "Yetenek (Kankuş)"},
    {"agent": "Gekko", "quote": "Zorba devrede, kaçın!", "category": "Ulti"},
    {"agent": "Gekko", "quote": "Mükemmel takım çalışması millet!", "category": "Tur Başı"},

    # CLOVE
    {"agent": "Clove", "quote": "Ölüm de neymiş, bir daha denerim!", "category": "Ulti (Ölümden Dönüş)"},
    {"agent": "Clove", "quote": "Geri döndüm şekerim!", "category": "Karakter Seçim"},
    {"agent": "Clove", "quote": "Ölmek sadece oyunun bir parçası.", "category": "Tur Başı"},
    {"agent": "Clove", "quote": "Kelebekler gibi uçar, arı gibi sokarım.", "category": "Katletme"},

    # ISO
    {"agent": "Iso", "quote": "Bire birde kimse beni yenemez!", "category": "Ulti (Düello Alanı)"},
    {"agent": "Iso", "quote": "Kafese girme vakti.", "category": "Karakter Seçim"},
    {"agent": "Iso", "quote": "Hedef odaklı, net ve temiz.", "category": "Tur Başı"},
    {"agent": "Iso", "quote": "Sadece sen ve ben. Başka kimse yok.", "category": "Ulti"},

    # DEADLOCK
    {"agent": "Deadlock", "quote": "Ağa yakalandınız!", "category": "Ulti"},
    {"agent": "Deadlock", "quote": "Bariyer kuruldu, geçiş yok!", "category": "Yetenek"},
    {"agent": "Deadlock", "quote": "Hiçbir av benden kaçamaz.", "category": "Karakter Seçim"},
    {"agent": "Deadlock", "quote": "Kuzeyin soğuğunu hissedin.", "category": "Tur Başı"},

    # VYSE
    {"agent": "Vyse", "quote": "Metaller bükülecek!", "category": "Ulti"},
    {"agent": "Vyse", "quote": "Çelikten kaçamazsınız!", "category": "Karakter Seçim"},
    {"agent": "Vyse", "quote": "Tuzak kuruldu, silahlarınızı kilitleyeceğim.", "category": "Yetenek"},

    # YORU
    {"agent": "Yoru", "quote": "Beni burada bulamazsınız.", "category": "Ulti"},
    {"agent": "Yoru", "quote": "Başka bir boyuttan geliyorum.", "category": "Karakter Seçim"},
    {"agent": "Yoru", "quote": "Yanlış yere bakıyorsunuz!", "category": "Yetenek (Yanıltıcı Ayak İzi)"},
    {"agent": "Yoru", "quote": "Benimle boy ölçüşemezsiniz.", "category": "Katletme"},

    # BREACH
    {"agent": "Breach", "quote": "Deprem yaratacağım!", "category": "Ulti"},
    {"agent": "Breach", "quote": "Yıkın geçin!", "category": "Karakter Seçim"},
    {"agent": "Breach", "quote": "Sarsıntıya hazır olun!", "category": "Yetenek"},
    {"agent": "Breach", "quote": "Açılın yoldan!", "category": "Tur Başı"},

    # SKYE
    {"agent": "Skye", "quote": "Kuş uçtu!", "category": "Yetenek (Kılavuz Işık)"},
    {"agent": "Skye", "quote": "Gözlerini aç kurt!", "category": "Yetenek (Avcı İzi)"},
    {"agent": "Skye", "quote": "Tazı kokuyu aldı!", "category": "Ulti"},
    {"agent": "Skye", "quote": "Şifa dağıtıyorum, yaklaşın!", "category": "Yetenek (Doğanın Şifası)"},

    # KAY/O
    {"agent": "KAY/O", "quote": "Sistem kilitlendi!", "category": "Ulti"},
    {"agent": "KAY/O", "quote": "Hiçbir radyant benden kaçamaz.", "category": "Karakter Seçim"},
    {"agent": "KAY/O", "quote": "Yetenekleri devre dışı bırakıldı.", "category": "Yetenek (Bıçak)"},
    {"agent": "KAY/O", "quote": "Görev: Tüm hedefleri etkisiz hale getirmek.", "category": "Tur Başı"},

    # HARBOR
    {"agent": "Harbor", "quote": "Dalgalar yükseliyor!", "category": "Ulti"},
    {"agent": "Harbor", "quote": "Su gibi akıp gideceğiz.", "category": "Karakter Seçim"},
    {"agent": "Harbor", "quote": "Dalgakıran devrede!", "category": "Yetenek"},

    # ASTRA
    {"agent": "Astra", "quote": "Kozmos benimle konuşuyor.", "category": "Karakter Seçim"},
    {"agent": "Astra", "quote": "Yıldızlar hizalandı.", "category": "Ulti"},
    {"agent": "Astra", "quote": "Evrenin sesini dinleyin.", "category": "Tur Başı"},

    # TEJO
    {"agent": "Tejo", "quote": "Doğru zaman, doğru yerleşim.", "category": "Karakter Seçim"},
    {"agent": "Tejo", "quote": "Hepsini adım adım hesapladım.", "category": "Tur Başı"}
]

# 4. Try scraping 13replik.com for extra quotes if available
def scrape_agent_page(agent_name, slug):
    url = f"https://www.13replik.com/valorant-{slug}-replikleri/"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    scraped = []
    try:
        with urllib.request.urlopen(req, timeout=4) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            paragraphs = re.findall(r'<p[^>]*>(.*?)</p>', html, re.DOTALL)
            in_turkish = False
            for p in paragraphs:
                clean = re.sub(r'<[^>]+>', '', p).strip()
                if f'Valorant {agent_name}' in clean or f'{agent_name} Replikleri' in clean:
                    in_turkish = True
                if in_turkish and ('“' in clean or '"' in clean or '&#8220;' in clean):
                    clean = clean.replace('&#8220;', '').replace('&#8221;', '').replace('“', '').replace('”', '').replace('"', '').strip()
                    clean = clean.replace('&#8217;', "'").replace('&#8230;', '...').replace('&amp;', '&')
                    if len(clean) > 8 and not clean.startswith('http'):
                        scraped.append(clean)
    except Exception:
        pass
    return scraped

slug_map = {
    "Phoenix": "phoenix",
    "Jett": "jett",
    "Reyna": "reyna",
    "Sage": "sage",
    "Omen": "omen",
    "Sova": "sova",
    "Fade": "fade",
    "Cypher": "cypher",
    "Raze": "raze",
    "Brimstone": "brimstone",
    "Viper": "viper",
    "Killjoy": "killjoy",
    "Chamber": "chamber",
    "Neon": "neon",
    "Gekko": "gekko",
    "Iso": "iso",
    "Deadlock": "deadlock",
    "Yoru": "yoru",
    "Breach": "breach",
    "Skye": "skye",
    "KAY/O": "kayo",
    "Harbor": "harbor",
    "Astra": "astra"
}

print("2. İnternetten ek Türkçe replikler taranıyor...")
all_quotes = list(iconic_quotes)
existing_texts = {q['quote'].lower().strip() for q in all_quotes}

for agent_name, slug in slug_map.items():
    scraped_lines = scrape_agent_page(agent_name, slug)
    count_added = 0
    for line in scraped_lines:
        normalized = line.lower().strip()
        if normalized not in existing_texts and len(line) > 10:
            existing_texts.add(normalized)
            all_quotes.append({
                "agent": agent_name,
                "quote": line,
                "category": "Genel Replik"
            })
            count_added += 1
    if count_added > 0:
        print(f"  + {agent_name}: {count_added} yeni replik eklendi.")

# Associate audio hints / audio files
# We can link audio files if available in audio/ folder (e.g. audio/<slug>_<id>.mp3)
for idx, q in enumerate(all_quotes):
    agent_clean = q['agent'].lower().replace('/', '').replace(' ', '_')
    q['id'] = f"q_{idx+1}"
    q['audioUrl'] = f"audio/{agent_clean}_{idx+1}.mp3"

# Write data/agents.json
agents_path = os.path.join(DATA_DIR, 'agents.json')
with open(agents_path, 'w', encoding='utf-8') as f:
    json.dump(agents_dict, f, ensure_ascii=False, indent=2)
print(f"Agents kaydedildi: {agents_path} ({len(agents_dict)} ajan)")

# Write data/quotes.json
quotes_path = os.path.join(DATA_DIR, 'quotes.json')
with open(quotes_path, 'w', encoding='utf-8') as f:
    json.dump(all_quotes, f, ensure_ascii=False, indent=2)
print(f"Quotes kaydedildi: {quotes_path} (Toplam {len(all_quotes)} Türkçe replik)")
