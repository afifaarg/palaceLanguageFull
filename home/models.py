from django.db import models

from wagtail.models import Page
from wagtail.fields import StreamField, RichTextField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.images.blocks import ImageChooserBlock
from wagtail.blocks import (
    CharBlock,
    TextBlock,
    StructBlock,
    StreamBlock,
    ListBlock,
)
from wagtail.snippets.models import register_snippet
from modelcluster.fields import ParentalManyToManyField

# Testimonial Snippet (for reusable testimonials)
@register_snippet
class Testimonial(models.Model):
    name = models.CharField(max_length=255)
    quote = models.TextField()

    panels = [
        FieldPanel("name"),
        FieldPanel("quote"),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Testimonial"
        verbose_name_plural = "Testimonials"

# HomePage Model
class HomePage(Page):
    # Hero Section
    hero_background_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    hero_heading = models.CharField(max_length=255, blank=True)
    hero_subheading = models.CharField(max_length=255, blank=True)

    # Palace Language Section
    palace_language_title = models.CharField(max_length=255, blank=True)
    palace_language_description = RichTextField(blank=True)
    palace_language_features = StreamField(
        [
            ("feature", StructBlock([
                ("icon", CharBlock(required=True)),
                ("title", CharBlock(required=True)),
                ("text", TextBlock(required=True)),
            ]))
        ],
        use_json_field=True,
        blank=True,
    )

    # About Us Section
    about_us_title = models.CharField(max_length=255, blank=True)
    about_us_description = RichTextField(blank=True)

    # Add-Ons Section
    add_ons = StreamField(
        [
            ("add_on", StructBlock([
                ("image_or_video", ImageChooserBlock(required=True)),
                ("title", CharBlock(required=True)),
                ("text", TextBlock(required=True)),
            ]))
        ],
        use_json_field=True,
        blank=True,
    )

    # Testimonials Section
    testimonials = ParentalManyToManyField("home.Testimonial", blank=True)

    # Trusted by Brands Section
    trusted_by_brands = StreamField(
        [
            ("brand", StructBlock([
                ("logo", ImageChooserBlock(required=True)),
                ("name", CharBlock(required=True)),
            ]))
        ],
        use_json_field=True,
        blank=True,
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("hero_background_image"),
                FieldPanel("hero_heading"),
                FieldPanel("hero_subheading"),
            ],
            heading="Hero Section",
        ),
        MultiFieldPanel(
            [
                FieldPanel("palace_language_title"),
                FieldPanel("palace_language_description"),
                FieldPanel("palace_language_features"),
            ],
            heading="Palace Language Section",
        ),
        MultiFieldPanel(
            [
                FieldPanel("about_us_title"),
                FieldPanel("about_us_description"),
            ],
            heading="About Us Section",
        ),
        MultiFieldPanel(
            [
                FieldPanel("add_ons"),
            ],
            heading="Add-Ons Section",
        ),
        MultiFieldPanel(
            [
                FieldPanel("testimonials"),
            ],
            heading="Testimonials Section",
        ),
        MultiFieldPanel(
            [
                FieldPanel("trusted_by_brands"),
            ],
            heading="Trusted by Brands Section",
        ),
    ]