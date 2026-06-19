# One-off script: fix SEO branding across ALL records by string replacement.
# Run with:  python fix_seo.py  (on the server, inside the virtualenv)
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')
django.setup()

from home.models import Seo

# Old -> New replacements applied to every title/description field.
# Order matters: more specific patterns first.
REPLACEMENTS = [
    # --- studio name variants ---
    ('Tattoo SK Workshop',          'Andrejs Tattoo'),
    ('Tatoo SK Workshop',           'Andrejs Tattoo'),
    ('Tatovering SK Workshop',      'Andrejs Tattoo'),
    ('Tattoo Sk Workshop',          'Andrejs Tattoo'),
    ('tatoveringsstudioet Tatoo SK Workshop', 'tatoveringsstudioet Andrejs Tattoo'),
    # --- location ---
    ('Fetsund Fetveien',            'Solheimsgata 1, Lillestrøm'),
    ('i Fetsund ved Oslo',          'i Lillestrøm ved Oslo'),
    ('i Fetsund',                   'i Lillestrøm'),
    ('Fetsund',                     'Lillestrøm'),
    # --- dash style (plain hyphen -> en-dash in titles) ---
    (' - Andrejs Tattoo',           ' – Andrejs Tattoo'),
    (' - Tatovering',               ' – Tatovering'),
]

FIELDS = [
    'title_en', 'description_en',
    'title_no', 'description_no',
    'keywords_en', 'keywords_no',
]

changed = 0
for seo in Seo.objects.all():
    dirty = False
    for field in FIELDS:
        original = getattr(seo, field) or ''
        updated = original
        for old, new in REPLACEMENTS:
            updated = updated.replace(old, new)
        if updated != original:
            setattr(seo, field, updated)
            dirty = True
    if dirty:
        seo.save()
        changed += 1
        print(f'  [FIXED] id={seo.id} | {seo.title_no or seo.title_en}')
    else:
        print(f'  [OK]    id={seo.id} | {seo.title_no or seo.title_en}')

print(f'\nDone. {changed} record(s) updated.')
