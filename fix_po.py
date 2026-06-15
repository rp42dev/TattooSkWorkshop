po_path = r"d:\GitHub\TattooSkWorkshop\dproject\locale\no\LC_MESSAGES\django.po"

with open(po_path, 'r', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()

translations = {
    "Home": "Hjem",
    "About Us": "Om oss",
    "Gallery": "Galleri",
    "Prices": "Priser",
    "Aftercare": "Ettervern",
    "FAQ": "FAQ",
    "Book Appointment": "Bestill time",
    "Get in Touch": "Ta kontakt",
    "Opening Hours": "Åpningstider",
    "Mon - Fri": "Man - Fre",
    "Saturday": "Lørdag",
    "Sunday": "Søndag",
    "Norway": "Norge",
    "Explore": "Utforsk",
    "Opening hours": "Åpningstider",
    "Monday - Friday": "Mandag - Fredag",
    "Contact": "Ta kontakt med",
}

new_lines = []
i = 0
while i < len(lines):
    line = lines[i]
    new_lines.append(line)
    if line.startswith('msgid "'):
        msgid = line.split('"')[1]
        if msgid in translations:
            # next line should be msgstr
            if i+1 < len(lines) and lines[i+1].startswith('msgstr ""'):
                new_lines.append(f'msgstr "{translations[msgid]}"\n')
                i += 1 # skip original empty msgstr
    i += 1

with open(po_path, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("PO file filled.")
