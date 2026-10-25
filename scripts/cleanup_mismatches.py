import json, os, sys
sys.path.append('D:/code-projects/valorant-replik')
from scratch.verify_all_gender_matches import get_gender, gender_map

sys.stdout.reconfigure(encoding='utf-8')

DATA_PATH = "D:/code-projects/valorant-replik/data/quotes.json"
quotes = json.load(open(DATA_PATH, encoding='utf-8'))

# The 4 problematic quotes:
problem_ids = ['quote_16', 'quote_37', 'quote_41', 'quote_45']

clean_quotes = [q for q in quotes if q['id'] not in problem_ids]
print(f"Remaining clean quotes: {len(clean_quotes)}")

# Re-index cleanly from quote_1 to quote_N
for i, q in enumerate(clean_quotes, start=1):
    q['id'] = f"quote_{i}"

# Now let's audit clean_quotes
mismatches = 0
for q in clean_quotes:
    mp3 = f"D:/code-projects/valorant-replik/{q['audioUrl']}"
    gen, dur = get_gender(mp3)
    exp = gender_map.get(q['agent'])
    if gen != exp:
        print(f"Mismatch: {q['id']} ({q['agent']}) Exp: {exp}, Got: {gen}")
        mismatches += 1

print(f"Mismatches in clean_quotes: {mismatches} / {len(clean_quotes)}")

with open(DATA_PATH, 'w', encoding='utf-8') as f:
    json.dump(clean_quotes, f, ensure_ascii=False, indent=2)

print("Saved clean_quotes to data/quotes.json!")
