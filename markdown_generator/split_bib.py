from pathlib import Path
import re

bib_path = Path("markdown_generator/pubs.bib")

text = bib_path.read_text(encoding="utf-8")

entries = text.split("@")

journal = []
proceedings = []

counter = 0

for e in entries:
    e = e.strip()
    if not e:
        continue

    entry = "@" + e
    low = e.lower()

    # -------- FIX DUPLICATE KEYS --------
    entry = re.sub(r'@\w+\{([^,]+),', f'@entry{{key{counter},', entry, count=1)
    counter += 1

    # -------- SPLIT TYPES --------
    if low.startswith("article"):
        journal.append(entry)
    elif low.startswith("inproceedings") or low.startswith("proceedings") or low.startswith("conference"):
        proceedings.append(entry)
    else:
        journal.append(entry)

# -------- WRITE OUTPUT --------
Path("markdown_generator/pubs.bib").write_text("\n\n".join(journal), encoding="utf-8")
Path("markdown_generator/proceedings.bib").write_text("\n\n".join(proceedings), encoding="utf-8")

print("✅ Done. pubs.bib and proceedings.bib created with unique keys.")
