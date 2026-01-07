from django.core.management.base import BaseCommand
from core.models import TeamMember

class Command(BaseCommand):
    help = 'Seeds initial leadership data for the About Us page'

    def handle(self, *args, **options):
        # Clear existing to avoid duplicates if needed, or just get_or_create
        TeamMember.objects.all().delete()
        
        members = [
            {
                "name": "Rob Trent",
                "role": "Founder & Managing Director",
                "bio": "Rob used his professional experience as a GIS specialist and his personal experience as a wheelchair user to create AccessAdvisr. His vision has driven the platform since its inception on the Ordnance Survey GeoVation challenge. Even in retirement, he remains active in meaningful projects that drive inclusion.\n\nA lifelong supporter of AFC Bournemouth, Rob has worked with the Football Stadium Advisory Design Council and the Football Foundation to improve stadium accessibility nationwide. He currently chairs Toucan Diversity Training and is an accomplished mouth painter with the Mouth and Foot Painting Artists.",
                "linkedin_url": "https://www.linkedin.com/in/robtrent-accessadvisr/",
                "order": 1
            },
            {
                "name": "Dr. Shah Siddiqui",
                "role": "Founder & CEO",
                "bio": "Dr. Shah is a visionary tech entrepreneur and AI strategist with over 20 years of experience. He is recognized for driving data-driven growth and building scalable ventures with long-term impact.\n\nAs the founder of GenZ Marketing Agency, Time Research & Innovation (Tri), and other pioneering organizations, he leverages technology for smarter business decisions. He serves as a mentor and board member for several organizations including Solent Partners and the Exeter Entrepreneurs Society.",
                "linkedin_url": "https://www.linkedin.com/in/dr-shah-siddiqui/",
                "order": 2
            }
        ]

        for m_data in members:
            member = TeamMember.objects.create(**m_data)
            self.stdout.write(self.style.SUCCESS(f'Successfully created team member: {member.name}'))
