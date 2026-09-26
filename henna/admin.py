from django.contrib import admin
from .models import Category, HennaDesign, Product, HomePageContent, AboutPageContent, BusinessSettings


# ---------------------------------------------------------------------------
# Business Settings — Phone number, Instagram, Business Name
# ---------------------------------------------------------------------------

@admin.register(BusinessSettings)
class BusinessSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ("📱 WhatsApp Contact", {
            "fields": ("whatsapp_number", "whatsapp_display"),
            "description": (
                "Change your WhatsApp number here. "
                "<b>whatsapp_number</b>: digits only with country code (e.g. 919025249906). "
                "<b>whatsapp_display</b>: formatted for display (e.g. +91 90252 49906)."
            ),
        }),
        ("🏷️ Business Identity", {
            "fields": ("business_name", "footer_tagline"),
        }),
        ("📸 Instagram", {
            "fields": ("instagram_handle", "instagram_url"),
        }),
    )

    def has_add_permission(self, request):
        return not BusinessSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        obj = BusinessSettings.load()
        return super().changeform_view(request, str(obj.pk), form_url, extra_context)





# ---------------------------------------------------------------------------
# Existing content models
# ---------------------------------------------------------------------------

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'display_order', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    ordering = ('display_order', 'name')


@admin.register(HennaDesign)
class HennaDesignAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'is_featured', 'display_order', 'created_at')
    list_filter = ('category', 'is_featured')
    search_fields = ('title', 'description')
    list_editable = ('price', 'is_featured', 'display_order')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'unit', 'badge', 'is_available', 'is_featured', 'display_order')
    list_filter = ('is_available', 'is_featured')
    search_fields = ('name', 'description')
    list_editable = ('price', 'unit', 'badge', 'is_available', 'is_featured', 'display_order')


# ---------------------------------------------------------------------------
# Page Content Singletons — only allow editing, not adding or deleting
# ---------------------------------------------------------------------------

class SingletonModelAdmin(admin.ModelAdmin):
    """
    Singleton admin: redirects 'add' to the existing record,
    hides delete action, and ensures exactly one object exists.
    """

    def has_add_permission(self, request):
        return not self.model.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def get_object(self, request, object_id, from_field=None):
        # Make sure pk=1 always exists
        self.model.load()
        return super().get_object(request, object_id, from_field)


@admin.register(HomePageContent)
class HomePageContentAdmin(SingletonModelAdmin):
    fieldsets = (
        ("🏠 Hero Section", {
            "fields": (
                "hero_title",
                "hero_description",
                "hero_image",
            ),
            "description": "Content shown in the large hero banner at the top of the home page.",
        }),
        ("📊 Statistics Strip", {
            "fields": (
                ("stat1_number", "stat1_label"),
                ("stat2_number", "stat2_label"),
                ("stat3_number", "stat3_label"),
                ("stat4_number", "stat4_label"),
            ),
            "description": "Four small stat pills shown beneath the hero buttons.",
        }),
        ("✅ Trust / Why Choose Us Cards", {
            "fields": (
                ("trust1_icon", "trust1_heading"),
                "trust1_text",
                ("trust2_icon", "trust2_heading"),
                "trust2_text",
                ("trust3_icon", "trust3_heading"),
                "trust3_text",
                ("trust4_icon", "trust4_heading"),
                "trust4_text",
            ),
        }),
        ("📣 Call-to-Action Banner", {
            "fields": (
                "cta_heading",
                "cta_subtext",
            ),
        }),
    )

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        # Always edit pk=1
        obj = HomePageContent.load()
        return super().changeform_view(request, str(obj.pk), form_url, extra_context)


@admin.register(AboutPageContent)
class AboutPageContentAdmin(SingletonModelAdmin):
    fieldsets = (
        ("📄 Page Header", {
            "fields": (
                "page_tag",
                "page_title",
                "page_subtitle",
            ),
        }),
        ("👩‍🎨 Artist Introduction", {
            "fields": (
                "artist_image",
                "experience_years",
                "section_tag",
                "artist_heading",
                "intro_lead",
                "intro_body1",
                "intro_body2",
            ),
        }),
        ("📊 Statistics", {
            "fields": (
                ("stat1_number", "stat1_label"),
                ("stat2_number", "stat2_label"),
                ("stat3_number", "stat3_label"),
            ),
        }),
        ("💎 Values / USP Boxes", {
            "fields": (
                ("value1_icon", "value1_heading"),
                "value1_text",
                ("value2_icon", "value2_heading"),
                "value2_text",
                ("value3_icon", "value3_heading"),
                "value3_text",
            ),
        }),
    )

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        # Always edit pk=1
        obj = AboutPageContent.load()
        return super().changeform_view(request, str(obj.pk), form_url, extra_context)
