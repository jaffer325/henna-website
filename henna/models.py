from django.db import models
from django.utils.text import slugify


# ---------------------------------------------------------------------------
# Singleton helpers for admin-editable page content
# ---------------------------------------------------------------------------

class SingletonModel(models.Model):
    """
    Abstract base for singleton models (only one row, pk=1).
    Use MyModel.load() to always get the single instance (creates defaults if missing).
    """

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass  # Prevent deletion from admin

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


# ---------------------------------------------------------------------------
# Business Settings (Phone, Instagram, Business Name — all editable from admin)
# ---------------------------------------------------------------------------

class BusinessSettings(SingletonModel):
    """
    Global business contact settings editable from the admin panel.
    These override the values in settings.py at runtime.
    """
    business_name = models.CharField(
        max_length=100,
        default="Afsha's Henna Art",
        help_text="Business name shown in the navbar, footer, and page titles.",
    )
    whatsapp_number = models.CharField(
        max_length=20,
        default="9025249906",
        help_text=(
            "WhatsApp number WITHOUT '+' or spaces. "
            "Include country code. Example: 919025249906 for +91 90252 49906."
        ),
    )
    whatsapp_display = models.CharField(
        max_length=30,
        default="+91 90252 49906",
        help_text="Formatted number shown on buttons, e.g. '+91 90252 49906'.",
    )
    instagram_handle = models.CharField(
        max_length=60,
        default="afshanashahul",
        help_text="Instagram username without '@', e.g. afshanashahul",
    )
    instagram_url = models.URLField(
        default="https://www.instagram.com/afshanashahul/",
        help_text="Full Instagram profile URL.",
    )
    footer_tagline = models.TextField(
        default=(
            "Handcrafted natural henna artistry for brides, festive occasions, "
            "and celebratory milestones. Made exclusively with 100% pure organic Rajasthani henna."
        ),
        help_text="Short tagline shown in the footer below the business name.",
    )

    class Meta:
        verbose_name = "Business Settings"
        verbose_name_plural = "Business Settings"

    def __str__(self):
        return f"{self.business_name} — WhatsApp: {self.whatsapp_display}"


# ---------------------------------------------------------------------------
# Home Page Content
# ---------------------------------------------------------------------------

class HomePageContent(SingletonModel):
    """Admin-editable content for the Home (index) page."""

    # Hero Section
    hero_title = models.CharField(
        max_length=200,
        default="Exquisite Henna Artistry for Your Most Cherished Celebrations",
        help_text="Main headline shown in the hero section.",
    )
    hero_description = models.TextField(
        default=(
            "Transform your special moments with handcrafted bridal, Arabic, "
            "traditional, and contemporary mehndi. We also formulate fresh, "
            "organic henna cones delivering a rich dark mahogany stain with zero chemicals."
        ),
        help_text="Short paragraph below the hero headline.",
    )
    hero_image = models.ImageField(
        upload_to="home/",
        blank=True,
        null=True,
        help_text="Hero section photo. Leave empty to use the default image.",
    )

    # Statistics Strip
    stat1_number = models.CharField(max_length=20, default="500+", help_text="e.g. 500+")
    stat1_label = models.CharField(max_length=50, default="Happy Brides")
    stat2_number = models.CharField(max_length=20, default="100%")
    stat2_label = models.CharField(max_length=50, default="Pure Organic")
    stat3_number = models.CharField(max_length=20, default="5+ Yrs")
    stat3_label = models.CharField(max_length=50, default="Experience")
    stat4_number = models.CharField(max_length=20, default="Dark")
    stat4_label = models.CharField(max_length=50, default="Stain Guarantee")

    # Trust / Why Choose Us cards
    trust1_icon = models.CharField(max_length=10, default="🌱", help_text="Emoji icon")
    trust1_heading = models.CharField(max_length=100, default="100% Organic & Chemical-Free")
    trust1_text = models.TextField(
        default="No PPD, no synthetic dyes, and no harsh preservatives. Freshly prepared with skin-loving pure essential oils."
    )

    trust2_icon = models.CharField(max_length=10, default="✨")
    trust2_heading = models.CharField(max_length=100, default="Rich Deep Burgundy Stain")
    trust2_text = models.TextField(
        default="Specially curated Sojat henna guarantees an intensely rich, dark reddish-brown stain that lasts for weeks."
    )

    trust3_icon = models.CharField(max_length=10, default="🎨")
    trust3_heading = models.CharField(max_length=100, default="Personalized Artistry")
    trust3_text = models.TextField(
        default="Every bride is unique. From royal motifs to delicate contemporary trails, designs are personalized to your vision."
    )

    trust4_icon = models.CharField(max_length=10, default="💬")
    trust4_heading = models.CharField(max_length=100, default="Direct WhatsApp Support")
    trust4_text = models.TextField(
        default="Chat directly with Afsha for consultation, design previews, custom cone orders, and bridal bookings."
    )

    # CTA Banner
    cta_heading = models.CharField(
        max_length=200,
        default="Planning a Wedding, Festival, or Family Celebration?",
    )
    cta_subtext = models.TextField(
        default="Book your bridal henna slots or get fresh handmade cones delivered right to your doorstep."
    )

    class Meta:
        verbose_name = "Home Page Content"
        verbose_name_plural = "Home Page Content"

    def __str__(self):
        return "Home Page Content"

    @property
    def hero_image_url(self):
        if self.hero_image:
            return self.hero_image.url
        return "/static/images/hero-henna1.png"


# ---------------------------------------------------------------------------
# About Page Content
# ---------------------------------------------------------------------------

class AboutPageContent(SingletonModel):
    """Admin-editable content for the About page."""

    # Hero / Page Header
    page_tag = models.CharField(
        max_length=80,
        default="OUR STORY & PASSION",
        help_text="Small tag above the page title (all caps recommended).",
    )
    page_title = models.CharField(
        max_length=200,
        default="Handcrafting Memories with Henna",
    )
    page_subtitle = models.TextField(
        default=(
            "Celebrating heritage, elegance, and pure botanicals through "
            "authentic bridal mehndi and handcrafted natural henna cones."
        )
    )

    # Artist intro section
    artist_image = models.ImageField(
        upload_to="about/",
        blank=True,
        null=True,
        help_text="Portrait photo of the artist. Leave empty for the default image.",
    )
    experience_years = models.CharField(
        max_length=10,
        default="5+",
        help_text="Number shown on the experience badge, e.g. '5+' or '7'.",
    )
    section_tag = models.CharField(max_length=80, default="MEET THE ARTIST")
    artist_heading = models.CharField(
        max_length=200,
        default="Creating Exquisite Henna Art with Devotion",
    )
    intro_lead = models.TextField(
        default=(
            "Welcome to Afsha's Henna Art. What began as a personal passion for "
            "intricate Indian and Arabic patterns has blossomed into an exclusive "
            "henna studio trusted by hundreds of brides and families across the region."
        )
    )
    intro_body1 = models.TextField(
        default=(
            "We specialize in creating tailored, high-detail mehndi for weddings, "
            "engagements, baby showers, and festive occasions. Every single design is "
            "customized to harmonize with your bridal attire, personal motifs, and celebratory theme."
        )
    )
    intro_body2 = models.TextField(
        default=(
            "Beyond artistry, we take immense pride in our fresh, handmade organic henna cones. "
            "We refuse to use commercial chemical cones loaded with toxic dyes and preservatives. "
            "Every cone is freshly hand-rolled, packed with triple-sifted Sojat henna powder and "
            "therapeutic-grade cajeput and eucalyptus oils for a deep, rich, long-lasting burgundy stain."
        )
    )

    # Stats
    stat1_number = models.CharField(max_length=20, default="500+")
    stat1_label = models.CharField(max_length=50, default="Happy Brides")
    stat2_number = models.CharField(max_length=20, default="2,500+")
    stat2_label = models.CharField(max_length=50, default="Cones Rolled")
    stat3_number = models.CharField(max_length=20, default="100%")
    stat3_label = models.CharField(max_length=50, default="Chemical-Free")

    # Values / USP boxes
    value1_icon = models.CharField(max_length=10, default="🌿")
    value1_heading = models.CharField(max_length=100, default="Purity in Ingredients")
    value1_text = models.TextField(
        default="Pure Rajasthani henna leaves, eucalyptus, tea tree, and cajeput oil. No black henna, no kerosene, no harmful chemicals."
    )

    value2_icon = models.CharField(max_length=10, default="⏱️")
    value2_heading = models.CharField(max_length=100, default="Punctual & Professional")
    value2_text = models.TextField(
        default="We respect the sacred timeline of your wedding festivities, ensuring calm, timely, and flawless execution on your big day."
    )

    value3_icon = models.CharField(max_length=10, default="💍")
    value3_heading = models.CharField(max_length=100, default="Bespoke Love Stories")
    value3_text = models.TextField(
        default="Incorporate initials, portraits, proposal dates, and sacred motifs into your bridal mehndi design."
    )

    class Meta:
        verbose_name = "About Page Content"
        verbose_name_plural = "About Page Content"

    def __str__(self):
        return "About Page Content"

    @property
    def artist_image_url(self):
        if self.artist_image:
            return self.artist_image.url
        return "/static/images/hero-henna1.png"

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    display_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['display_order', 'name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class HennaDesign(models.Model):
    title = models.CharField(max_length=150)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='designs')
    description = models.TextField(help_text="Short description of the design and placement.")
    price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, help_text="Starting or fixed price in INR (optional)")
    image = models.ImageField(upload_to='designs/', blank=True, null=True)
    static_image = models.CharField(max_length=255, blank=True, default='', help_text="Relative static image path e.g. 'images/designs/bridal.jpg'")
    is_featured = models.BooleanField(default=False, help_text="Showcase on the homepage")
    display_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['display_order', '-created_at']

    def __str__(self):
        return f"{self.title} ({self.category.name})"

    @property
    def image_url(self):
        if self.image:
            return self.image.url
        if self.static_image:
            return f"/static/{self.static_image}"
        return "/static/images/hero-henna1.png"


class Product(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(help_text="Detailed description of the product ingredients and use.")
    price = models.DecimalField(max_digits=8, decimal_places=2, help_text="Price in INR")
    unit = models.CharField(max_length=60, default="Per Cone", help_text="e.g. Per Cone, 100g Pack, Pack of 5, Complete Kit")
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    static_image = models.CharField(max_length=255, blank=True, default='', help_text="Relative static image path e.g. 'images/products/cone.jpg'")
    badge = models.CharField(max_length=50, blank=True, help_text="Highlight badge like '100% Organic', 'Bestseller'")
    is_available = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False, help_text="Showcase on the homepage")
    display_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['display_order', '-created_at']

    def __str__(self):
        return f"{self.name} - ₹{self.price}"

    @property
    def image_url(self):
        if self.image:
            return self.image.url
        if self.static_image:
            return f"/static/{self.static_image}"
        return "/static/images/image.png"
