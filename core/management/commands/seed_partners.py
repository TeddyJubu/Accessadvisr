from django.core.management.base import BaseCommand
from core.models import Partner

class Command(BaseCommand):
    help = 'Seeds initial partner and sponsor data'

    def handle(self, *args, **kwargs):
        sponsors = [
            {
                "name": "HeX Productions",
                "type": "sponsor",
                "description": "HeX Productions, a UK-based digital accessibility agency, delivers inclusive web solutions, accessibility audits, and training to ensure digital services are accessible to everyone.",
                "website_url": "https://www.hexproductions.co.uk/",
                "order": 1
            },
            {
                "name": "Pressalit",
                "type": "sponsor",
                "description": "Pressalit, a Danish leader in accessible bathroom solutions and height-adjustable kitchen systems, provides high-quality products designed to enhance independence for people with disabilities.",
                "website_url": "https://www.pressalit.com/",
                "order": 2
            },
            {
                "name": "GenZ Marketing",
                "type": "sponsor",
                "description": "UK’s leading digital agency powering the movement of AccessAdvisr through expert marketing and strategic partnership support.",
                "website_url": "https://genzmarketing.co.uk/",
                "order": 3
            },
        ]

        partners = [
            {"name": "Enable My Trip", "type": "partner", "website_url": "https://enablemytrip.org.uk/", "order": 1},
            {"name": "Madeira Acessivel By Wheelchair", "type": "partner", "website_url": "https://www.madeirabywheelchair.com/", "order": 2},
            {"name": "ITP (Integrated Transport Planning)", "type": "partner", "website_url": "https://itpworld.net/", "order": 3},
            {"name": "Taylor Made Wheelchairs", "type": "partner", "website_url": "https://www.taylormadewheelchairs.com/", "order": 4},
            {"name": "Accessible Romania", "type": "partner", "website_url": "https://accessibleromania.com/", "order": 5},
            {"name": "Holiday Mobility Scooters Menorca", "type": "partner", "website_url": "https://www.holidaymobilitymenorca.com/", "order": 6},
            {"name": "Disability Roadmap CIC", "type": "partner", "website_url": "", "order": 7},
            {"name": "Seated Sewing", "type": "partner", "website_url": "https://seatedsewing.co.uk/", "order": 8},
            {"name": "Flat Spaces", "type": "partner", "website_url": "https://flatspaces.co.uk/", "order": 9},
            {"name": "Art for ACCESS AUSTRALIA", "type": "partner", "website_url": "", "order": 10},
            {"name": "Blue Badge Style", "type": "partner", "website_url": "https://bluebadgestyle.com/", "order": 11},
            {"name": "CityMaaS", "type": "partner", "website_url": "https://citymaas.io/", "order": 12},
            {"name": "WelcoMe", "type": "partner", "website_url": "https://www.wel-co.me/", "order": 13},
            {"name": "Fatcatz Mobility", "type": "partner", "website_url": "", "order": 14},
            {"name": "AccessibleTravel.Online", "type": "partner", "website_url": "https://accessibletravel.online/", "order": 15},
            {"name": "Toucan Diversity Training", "type": "partner", "website_url": "https://www.toucandiversity.org.uk/", "order": 16},
        ]

        # Create sponsors
        for s_data in sponsors:
            p, created = Partner.objects.update_or_create(
                name=s_data["name"],
                defaults=s_data
            )
            if created:
                self.stdout.write(f"Created sponsor: {p.name}")
        
        # Create partners
        for p_data in partners:
            p, created = Partner.objects.get_or_create(
                name=p_data["name"],
                defaults=p_data
            )
            if created:
                self.stdout.write(f"Created partner: {p.name}")

        self.stdout.write(self.style.SUCCESS('Successfully seeded partners and sponsors'))
