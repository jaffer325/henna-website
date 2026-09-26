from django.core.management.base import BaseCommand
from henna.models import Category, HennaDesign, Product

class Command(BaseCommand):
    help = "Seed initial henna designs, categories, and products"

    def handle(self, *args, **options):
        # 1. Categories
        categories_data = [
            ("Bridal Mehndi", "bridal-mehndi", 1),
            ("Arabic Mehndi", "arabic-mehndi", 2),
            ("Simple Mehndi", "simple-mehndi", 3),
            ("Traditional Mehndi", "traditional-mehndi", 4),
            ("Front Hand", "front-hand", 5),
            ("Back Hand", "back-hand", 6),
            ("Feet Mehndi", "feet-mehndi", 7),
        ]

        cat_map = {}
        for name, slug, order in categories_data:
            cat, created = Category.objects.get_or_create(
                slug=slug,
                defaults={'name': name, 'display_order': order}
            )
            cat.name = name
            cat.display_order = order
            cat.save()
            cat_map[slug] = cat
        self.stdout.write(self.style.SUCCESS(f"Saved {len(cat_map)} categories."))

        # 2. Henna Designs
        designs_data = [
            {
                "title": "Royal Heritage Bridal Mehndi",
                "category": cat_map["bridal-mehndi"],
                "description": "Full hand and forearm bridal composition with intricate mandala, dulha-dulhan motifs, and delicate mesh netting.",
                "price": 3500.00,
                "static_image": "images/designs/bridal_mehndi.jpg",
                "is_featured": True,
                "display_order": 1,
            },
            {
                "title": "Arabic Floral Trail Mehndi",
                "category": cat_map["arabic-mehndi"],
                "description": "Free-flowing shaded roses and floral vines arching diagonally from wrist to fingertip with bold outlines.",
                "price": 1200.00,
                "static_image": "images/designs/arabic_mehndi.jpg",
                "is_featured": True,
                "display_order": 2,
            },
            {
                "title": "Dainty Finger & Palm Mandala",
                "category": cat_map["simple-mehndi"],
                "description": "Minimalist boho-inspired central sun mandala with delicate finger vine accents. Ideal for parties and festivals.",
                "price": 600.00,
                "static_image": "images/designs/simple_mehndi.jpg",
                "is_featured": True,
                "display_order": 3,
            },
            {
                "title": "Classic Rajasthani Traditional Mehndi",
                "category": cat_map["traditional-mehndi"],
                "description": "Dense heritage peacocks, lotus petals, and check work symbolizing joy and prosperity.",
                "price": 2200.00,
                "static_image": "images/designs/traditional_mehndi.jpg",
                "is_featured": False,
                "display_order": 4,
            },
            {
                "title": "Intricate Full Front Palm Design",
                "category": cat_map["front-hand"],
                "description": "Deeply detailed front palm pattern extending to wrist, highlighting symmetry and botanical elegance.",
                "price": 950.00,
                "static_image": "images/designs/front_hand.jpg",
                "is_featured": False,
                "display_order": 5,
            },
            {
                "title": "Jeweled Glove Back Hand Mehndi",
                "category": cat_map["back-hand"],
                "description": "Exquisite hathphool-style jewelry lace on back of the hand connecting fingers with delicate bead chains.",
                "price": 900.00,
                "static_image": "images/designs/back_hand.jpg",
                "is_featured": True,
                "display_order": 6,
            },
            {
                "title": "Bridal Floral Anklet & Feet Mehndi",
                "category": cat_map["feet-mehndi"],
                "description": "Graceful bridal foot coverage with ornate payal anklet band and paisley toes design.",
                "price": 1800.00,
                "static_image": "images/designs/feet_mehndi.jpg",
                "is_featured": True,
                "display_order": 7,
            },
        ]

        for d in designs_data:
            HennaDesign.objects.update_or_create(
                title=d["title"],
                defaults=d
            )
        self.stdout.write(self.style.SUCCESS("Saved Henna Designs."))

        # 3. Products
        products_data = [
            {
                "name": "Bridal Henna Cone",
                "description": "Handcrafted fresh henna cone infused with pure Cajeput and Nilgiri essential oils. Formulated for ultra-dark stain for brides.",
                "price": 120.00,
                "unit": "Per Cone",
                "static_image": "images/products/bridal_cone.jpg",
                "badge": "Bridal Special",
                "is_available": True,
                "is_featured": True,
                "display_order": 1,
            },
            {
                "name": "Premium Natural Henna Cone",
                "description": "Smooth silky consistency with 0.38mm precision pin. 100% chemical-free and safe for children and sensitive skin.",
                "price": 100.00,
                "unit": "Per Cone",
                "static_image": "images/products/premium_cone.jpg",
                "badge": "Bestseller",
                "is_available": True,
                "is_featured": True,
                "display_order": 2,
            },
            {
                "name": "Natural Henna Powder",
                "description": "100% pure triple cloth-sifted Sojat Rajasthani Lawsonia inermis powder. Mix with your own oils for vibrant color.",
                "price": 250.00,
                "unit": "200g Pack",
                "static_image": "images/products/henna_powder.jpg",
                "badge": "100% Organic",
                "is_available": True,
                "is_featured": True,
                "display_order": 3,
            },
            {
                "name": "Organic Henna Powder (Bulk)",
                "description": "Premium farm-sourced organic henna leaf powder in resealable moisture-lock craft pouch. Best for professional artists.",
                "price": 450.00,
                "unit": "500g Pack",
                "static_image": "images/products/organic_powder.jpg",
                "badge": "Artist Grade",
                "is_available": True,
                "is_featured": False,
                "display_order": 4,
            },
            {
                "name": "Henna Aftercare Oil",
                "description": "Herbal blend of eucalyptus, clove, and sweet almond oils. Darkens the stain and locks moisture for long-lasting color.",
                "price": 180.00,
                "unit": "30ml Dropper Bottle",
                "static_image": "images/products/bridal_cone.jpg",
                "badge": "Stain Booster",
                "is_available": True,
                "is_featured": True,
                "display_order": 5,
            },
            {
                "name": "Henna Artist Design Kit",
                "description": "Complete DIY starter kit: 4 fresh cones, aftercare oil, acrylic practice sheet, 2 designer stencils, and sealant spray.",
                "price": 599.00,
                "unit": "Complete Kit",
                "static_image": "images/products/henna_powder.jpg",
                "badge": "Value Pack",
                "is_available": True,
                "is_featured": True,
                "display_order": 6,
            },
        ]

        for p in products_data:
            Product.objects.update_or_create(
                name=p["name"],
                defaults=p
            )
        self.stdout.write(self.style.SUCCESS("Saved Products."))
