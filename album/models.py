from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.timezone import now
from django_resized import ResizedImageField
from pillow_heif import register_heif_opener
from django.utils.translation import gettext_lazy as _

from home.models import Seo, Page
register_heif_opener()


from dproject.constants import ASPECT_RATIOS, SIZES


class Artist(models.Model):
    """Artist model"""
    name = models.CharField(max_length=254)
    image = ResizedImageField(
        size=[2560, 2560], quality=100,
        upload_to='artist', blank=True, null=True)
    slug = models.SlugField(auto_created=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    order = models.IntegerField(blank=True, null=True)
    page = models.ForeignKey(
        Page, on_delete=models.CASCADE, blank=True, null=True)

    def get_absolute_url(self):
        return reverse("gallery", kwargs={"slug": self.slug})


    def get_friendly_name(self):
        return self.name  # Fixed: friendly_name field was missing

    def __str__(self):
        return self.name


class Album(models.Model):
    """Album model"""
    ASPECT_RATIOS = ASPECT_RATIOS
    SIZES = SIZES

    artist = models.ForeignKey(
        'Artist', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=254)
    description = models.TextField(blank=True, null=True)
    aspect_ratio = models.CharField(
        choices=ASPECT_RATIOS, max_length=20, default='original')
    image = ResizedImageField(
        size=[2560, 2560], quality=100, upload_to='album', blank=True, null=True)
    seo = models.ForeignKey(
        Seo, on_delete=models.CASCADE, blank=True, null=True)
    slug = models.SlugField(auto_created=True, blank=True, null=True)



    def _build_seo_strings(self):
        """Return (title_en, desc_en, title_no, desc_no) generated from album data."""
        name = self.name or 'Tattoo'
        artist_name = self.artist.name if self.artist else 'Andrejs Baranovs'

        title_en = f"{name} – Andrejs Tattoo | Custom Tattoo Lillestrøm"
        desc_en  = (
            f"Custom tattoo '{name}' by {artist_name} at Andrejs Tattoo in "
            f"Lillestrøm, Norway. Quality tattoos, coverups and unique designs. Book today!"
        )

        title_no = f"{name} – Andrejs Tattoo | Tilpasset tatovering Lillestrøm"
        desc_no  = (
            f"Tilpasset tatovering '{name}' av {artist_name} på Andrejs Tattoo i "
            f"Lillestrøm, Norge. Kvalitetstatoveringer, coverups og unike design. Bestill i dag!"
        )
        # Clamp descriptions to 160 chars (meta description limit)
        return title_en[:200], desc_en[:160], title_no[:200], desc_no[:160]

    def save(self, *args, **kwargs):
        """Auto-create or update the linked Seo record on every save."""
        from home.models import Seo as SeoModel
        title_en, desc_en, title_no, desc_no = self._build_seo_strings()

        if self.seo_id:
            # Update existing linked Seo record
            SeoModel.objects.filter(pk=self.seo_id).update(
                title_en=title_en, description_en=desc_en,
                title_no=title_no,  description_no=desc_no,
            )
        else:
            # Create a fresh Seo record and link it
            seo = SeoModel.objects.create(
                title_en=title_en, description_en=desc_en,
                title_no=title_no,  description_no=desc_no,
            )
            self.seo = seo

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("details", kwargs={"artist_slug": self.artist.slug, "slug": self.slug})

    def __str__(self):
        return self.name
