# One-off script: update all SEO records to reflect the new branding.
# Run with:  .venv/Scripts/python.exe fix_seo.py
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')
django.setup()

from home.models import Seo

updates = {
    # id: (title_en, description_en, title_no, description_no)

    # Gallery
    11: (
        "Gallery – Andrejs Tattoo | Custom Tattoos Lillestrøm",
        "Browse the tattoo gallery of Andrejs Baranovs. Tattoo artist in Lillestrøm, Norway. We create unique, custom tattoo designs tailored just for you.",
        "Galleri – Andrejs Tattoo | Tilpassede tatoveringer Lillestrøm",
        "En tatovering er den nye avhengigheten. Sjekk ut galleriet vårt og se arbeidet til tatoveringskunstneren vår Andrejs Baranovs, tatoveringsstudio i Lillestrøm.",
    ),

    # Location
    10: (
        "Location – Andrejs Tattoo | Custom Tattoos Lillestrøm",
        "Find us at Solheimsgata 1, 2000 Lillestrøm, Norway – just minutes from the city centre. Open every day, 7 days a week. Contact us now.",
        "Lokasjon – Andrejs Tattoo | Tilpassede tatoveringer Lillestrøm",
        "Vi holder til i Solheimsgata 1, 2000 Lillestrøm, Norge, kun noen minutter fra sentrum. Vi har åpent hver dag, 7 dager i uken. Kontakt oss nå.",
    ),

    # Home
    9: (
        "Andrejs Tattoo | Quality Tattoos and Tattoo Coverups Lillestrøm",
        "Tattoo studio in Lillestrøm, Norway. We specialise in quality tattoos, custom tattoos, coverups, scar cover-ups and more. Book an appointment today!",
        "Andrejs Tattoo | Kvalitetstatoveringer og Tattoo Coverups Lillestrøm",
        "Tatoveringsstudio i Lillestrøm, Norge. Vi er spesialister på kvalitetstatoveringer, tilpassede tatoveringer, coverups, arr cover-ups og mer. Bestill time i dag!",
    ),

    # FAQ
    8: (
        "FAQ – Andrejs Tattoo | Tattoo Studio in Lillestrøm near Oslo",
        "Frequently asked questions about tattooing and the Andrejs Tattoo studio in Lillestrøm near Oslo. Focused on quality and customer service.",
        "FAQ – Andrejs Tattoo | Tatovere deg i Lillestrøm ved Oslo",
        "Ofte stilte spørsmål om tatovering og tatoveringsstudioet Andrejs Tattoo i Lillestrøm ved Oslo. Med fokus på kvalitet og kundeservice.",
    ),

    # Aftercare
    7: (
        "Tattoo Aftercare – Andrejs Tattoo | Realism and Black & Grey Tattoos",
        "Our highest priority is to give you the best tattoo aftercare possible. We provide all the information you need to take care of your new tattoo.",
        "Tattoo ettervern – Andrejs Tattoo | Realisme og svarte og grå tatoveringer",
        "Vår høyeste prioritet er å gi deg den beste tatoveringsetterbehandlingen som mulig. Vi vil gi deg all informasjonen du trenger for å ta vare på tatoveringen din.",
    ),

    # Prices
    6: (
        "Prices – Andrejs Tattoo | Grey Wash Tattoos Lillestrøm",
        "Price list for tattoos at Andrejs Tattoo. We welcome you to our studio in Lillestrøm. Contact us for more information.",
        "Priser – Andrejs Tattoo | Grey wash tatoveringer Lillestrøm",
        "Prisliste for tatoveringer på Andrejs Tattoo. Vi ønsker deg velkommen til vårt studio i Lillestrøm. Ta kontakt med oss for mer informasjon.",
    ),

    # About
    5: (
        "About – Andrejs Tattoo | Tattoo Studio in Lillestrøm",
        "Andrejs Tattoo is a tattoo studio in Lillestrøm, Norway, located at Solheimsgata 1, 2000 Lillestrøm. Open every day. Contact us.",
        "Om – Andrejs Tattoo | Tatoveringsstudio i Lillestrøm",
        "Andrejs Tattoo er et tatoveringsstudio i Lillestrøm, Norge. Vi holder til i Solheimsgata 1, 2000 Lillestrøm, Norge. Vi har åpent hver dag. Kontakt oss.",
    ),
}

for seo_id, (title_en, desc_en, title_no, desc_no) in updates.items():
    try:
        seo = Seo.objects.get(pk=seo_id)
        seo.title_en = title_en
        seo.description_en = desc_en
        seo.title_no = title_no
        seo.description_no = desc_no
        seo.save()
        print(f"  [OK] id={seo_id} -> {title_en}")
    except Seo.DoesNotExist:
        print(f"  [SKIP] id={seo_id} not found")

print("\nAll done.")
