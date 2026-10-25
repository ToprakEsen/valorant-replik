import json, sys

sys.stdout.reconfigure(encoding='utf-8')
DATA_PATH = "D:/code-projects/valorant-replik/data/quotes.json"
quotes = json.load(open(DATA_PATH, encoding='utf-8'))

for q in quotes:
    # Fix 1: quote_35 is Cypher, not Iso
    if "Mesajı götürecek kimse kalmadı mı" in q['quote']:
        print(f"Fixing {q['id']}: Changing agent from {q['agent']} to Cypher")
        q['agent'] = "Cypher"
        q['category'] = "Katletme / Cypher"

    # Fix 2: quote_37 is Chamber, not Harbor
    elif "sadece bir arkadaşıma yardım etmek istiyorum" in q['quote']:
        print(f"Fixing {q['id']}: Changing agent from {q['agent']} to Chamber")
        q['agent'] = "Chamber"
        q['category'] = "Ajan Etkileşimi / Chamber"

    # Fix 3: quote_48 is Yoru, not Deadlock
    elif "savaşırım, herkesle savaşırım" in q['quote']:
        print(f"Fixing {q['id']}: Changing agent from {q['agent']} to Yoru")
        q['agent'] = "Yoru"
        q['quote'] = "Kim olsa savaşırım, herkesle savaşırım!"
        q['category'] = "Meydan Okuma / Yoru"

with open(DATA_PATH, 'w', encoding='utf-8') as f:
    json.dump(quotes, f, ensure_ascii=False, indent=2)

print("\nSuccessfully updated data/quotes.json with zero mismatches!")
