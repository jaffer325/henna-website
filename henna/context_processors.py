from django.conf import settings


def business_info(request):
    """
    Context processor providing global business and WhatsApp contact information.
    Reads from the BusinessSettings model in the database (admin-editable).
    Falls back to settings.py values if the DB record doesn't exist yet.
    """
    try:
        from .models import BusinessSettings
        biz = BusinessSettings.load()
        return {
            'BUSINESS_NAME': biz.business_name,
            'WHATSAPP_PHONE_NUMBER': biz.whatsapp_number,
            'WHATSAPP_DISPLAY_NUMBER': biz.whatsapp_display,
            'INSTAGRAM_HANDLE': biz.instagram_handle,
            'INSTAGRAM_URL': biz.instagram_url,
            'FOOTER_TAGLINE': biz.footer_tagline,
        }
    except Exception:
        # Fallback to settings.py values (safe during first migration)
        return {
            'BUSINESS_NAME': getattr(settings, 'BUSINESS_NAME', "Afsha's Henna Art"),
            'WHATSAPP_PHONE_NUMBER': getattr(settings, 'WHATSAPP_PHONE_NUMBER', '919025249906'),
            'WHATSAPP_DISPLAY_NUMBER': getattr(settings, 'WHATSAPP_DISPLAY_NUMBER', '+91 90252 49906'),
            'INSTAGRAM_HANDLE': getattr(settings, 'INSTAGRAM_HANDLE', 'afshanashahul'),
            'INSTAGRAM_URL': getattr(settings, 'INSTAGRAM_URL', 'https://www.instagram.com/afshanashahul/'),
            'FOOTER_TAGLINE': 'Handcrafted natural henna artistry for brides and festive occasions.',
        }
