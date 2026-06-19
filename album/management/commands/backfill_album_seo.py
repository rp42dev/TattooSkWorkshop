"""
Management command: backfill auto-generated SEO for all existing Album records.

Usage:
    python manage.py backfill_album_seo
    python manage.py backfill_album_seo --dry-run   # preview only, no DB writes
"""
from django.core.management.base import BaseCommand
from album.models import Album


class Command(BaseCommand):
    help = 'Auto-generate / update SEO title & description for every Album.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run', action='store_true',
            help='Print what would be changed without writing to the DB.',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        albums = Album.objects.select_related('artist', 'seo').all()
        total = albums.count()
        updated = 0

        self.stdout.write(f'Processing {total} album(s)...\n')

        for album in albums:
            title_en, desc_en, title_no, desc_no = album._build_seo_strings()

            if dry_run:
                self.stdout.write(
                    f'  [DRY] id={album.id} | {title_en}\n'
                    f'        {desc_en}\n'
                )
                continue

            # Trigger the save() which auto-creates/updates the Seo record.
            album.save()
            updated += 1
            self.stdout.write(self.style.SUCCESS(
                f'  [OK] id={album.id} | {album.name} -> seo id={album.seo_id}'
            ))

        if not dry_run:
            self.stdout.write(self.style.SUCCESS(
                f'\nDone. {updated}/{total} album(s) updated.'
            ))
