from django.core.management.base import BaseCommand
from core.models import SponsorshipPackage, DonationGoal
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Seeds sponsorship packages and donation goals'

    def handle(self, *args, **options):
        self.stdout.write('Seeding sponsorship packages...')
        
        packages = [
            {
                'name': 'Gateway Sponsor',
                'price': 500,
                'period': 'Yearly',
                'subheading': 'Perfect for small businesses or local organisations keen to support accessible travel.',
                'features': [
                    'Your logo displayed on our Supporters Page with a backlink to your website.',
                    '1 social media shout-out per month (Facebook + Instagram + LinkedIn).',
                    'Name mention at the end of 1 podcast or webinar per quarter.',
                    'Digital badge to display on your own website: Proud Supporter of AccessAdvisr.'
                ],
                'order': 1
            },
            {
                'name': 'Impact Sponsor',
                'price': 1500,
                'period': 'Yearly',
                'subheading': 'Ideal for regional and national brands wanting stronger visibility and engagement.',
                'features': [
                    'Logo featured on every podcast and webinar slide deck.',
                    'Name and logo mentioned verbally at start and end of podcasts and webinars.',
                    'Dedicated sponsor section on our website (logo, intro blurb, link).',
                    '1 social media posts every quater across Facebook, Instagram, YouTube Shorts, and LinkedIn, with sponsor tags.',
                    'Opportunity to provide 1 guest blog or video (up to 3 mins) on accessibility.',
                    'Access to periodic insights on community reach and engagement data.'
                ],
                'order': 2
            },
            {
                'name': 'Inclusion Sponsor',
                'price': 3000,
                'period': 'Yearly',
                'subheading': 'For companies seeking premium, long-term brand association with inclusive travel innovation.',
                'features': [
                    'Prominent logo placement on all AccessAdvisr web pages (footer + special sponsor section with video intro).',
                    'Logo and link included in every newsletter (monthly reach report).',
                    'Verbal and visual mention at 2 webinars/podcast/YouTube videos.',
                    '2 social media posts every quater, including YouTube Shorts, Facebook, Instagram, and LinkedIn.',
                    'Exclusive featured sponsor video (up to 5 mins) on our website sponsor page, shared to YouTube and Facebook.'
                ],
                'order': 3
            }
        ]

        for pkg_data in packages:
            pkg, created = SponsorshipPackage.objects.get_or_create(
                name=pkg_data['name'],
                defaults={
                    'slug': slugify(pkg_data['name']),
                    'price': pkg_data['price'],
                    'period': pkg_data['period'],
                    'subheading': pkg_data['subheading'],
                    'features': pkg_data['features'],
                    'order': pkg_data['order'],
                    'is_active': True
                }
            )
            if created:
                self.stdout.write(f"Created package: {pkg.name}")
            else:
                self.stdout.write(f"Package already exists: {pkg.name}")

        self.stdout.write('Seeding donation goals...')
        
        goals = [
            {
                'title': "Fundraiser for NBC's financial aid programme and contributing to the success of neurodivergent entrepreneurs",
                'description': "AccessAdvisr is dedicated to making the world more accessible for disabled people everywhere. Our platform allows users to share honest reviews about the accessibility of places, helping others make informed decisions before visiting. With over 2,600 reviews worldwide, we provide a free, reliable resource that empowers the disabled community. Running and improving this website comes with costs. Your donation helps us enhance features, introduce new tools, and ensure the site meets the latest accessibility standards.",
                'target_amount': 10000,
                'raised_amount': 0
            },
            {
                'title': "We need your support for organisational development",
                'description': "Running and improving this website comes with costs. Your donation helps us enhance features, introduce new tools, and ensure the site meets the latest accessibility standards. It allows us to expand our reach, improve user experience, and continue offering free, accurate information to those who need it most.",
                'target_amount': 5000,
                'raised_amount': 0
            },
            {
                'title': "We need your support for administration, mentoring and training programmes",
                'description': "By donating, you become part of a movement that values inclusion and accessibility. Your support not only funds website upgrades and maintenance but also strengthens a community dedicated to making travel and everyday experiences easier and more enjoyable for everyone. Every contribution, big or small, helps us grow and make a real difference.",
                'target_amount': 2000,
                'raised_amount': 0
            }
        ]

        for goal_data in goals:
            goal, created = DonationGoal.objects.get_or_create(
                title=goal_data['title'],
                defaults={
                    'slug': slugify(goal_data['title'])[:50],
                    'description': goal_data['description'],
                    'target_amount': goal_data['target_amount'],
                    'raised_amount': goal_data['raised_amount'],
                    'is_active': True
                }
            )
            if created:
                self.stdout.write(f"Created goal: {goal.title[:50]}...")
            else:
                self.stdout.write(f"Goal already exists: {goal.title[:50]}...")

        self.stdout.write(self.style.SUCCESS('Successfully seeded sponsorship and donation data'))
