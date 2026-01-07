from django.core.management.base import BaseCommand
from django.utils.text import slugify
from django.contrib.auth.models import User
from core.models import BlogCategory, BlogPost

class Command(BaseCommand):
    help = 'Seeds the database with initial blog categories and posts'

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding blog categories and posts...")
        
        # Create an admin user if not exists
        author, created = User.objects.get_or_create(username='admin')
        if created:
            author.set_password('admin123')
            author.is_staff = True
            author.is_superuser = True
            author.save()
            self.stdout.write(self.style.SUCCESS(f"Created author: {author.username}"))

        categories = [
            "Travel Guides",
            "Accessibility News",
            "Product Reviews",
            "Community Stories",
            "Top Lists"
        ]

        cat_objs = []
        for name in categories:
            cat, created = BlogCategory.objects.get_or_create(
                name=name,
                defaults={'slug': slugify(name)}
            )
            cat_objs.append(cat)
            if created:
                self.stdout.write(f"Created category: {name}")

        posts_data = [
            {
                "title": "Top Tips for Choosing Accessible Accommodation Easily",
                "category": "Travel Guides",
                "content": "Finding the right accessible accommodation can make a big difference in your travel experience. Whether you have mobility issues, use a wheelchair, or have other accessibility needs, planning ahead is key.\n\nFirst, always call the venue directly. Don't rely solely on online booking descriptions. Ask specific questions about door widths, grab bars, and elevator access. Second, look for real reviews from other disabled travellers. Sites like AccessAdvisr provide invaluable first-hand information that official websites often miss.",
                "excerpt": "Finding the right accessible accommodation can make a big difference in your travel experience. Learn how to pick the best spots."
            },
            {
                "title": "Enjoy Inclusive Dining at Accessible Restaurants Nearby",
                "category": "Top Lists",
                "content": "Eating out should be enjoyable for everyone, and accessible restaurants make dining possible for people with disabilities. These restaurants provide more than just ramps; they offer spacious layouts, accessible restrooms, and supportive staff.\n\nWhen looking for a place to eat, consider the atmosphere. Is it too loud for someone with sensory sensitivities? Is the lighting adequate? Our community has rated thousands of restaurants across London to help you find the perfect spot for your next meal.",
                "excerpt": "Eating out should be enjoyable for everyone. We've compiled a list of the most inclusive dining spots."
            },
            {
                "title": "Enjoy Hassle-Free Accessible Transport Wherever You Go",
                "category": "Accessibility News",
                "content": "Getting from one place to another should be easy for everyone. Accessible transport makes travel comfortable and safe for people with disabilities. From bus kneeling features to app-based taxi services with wheelchair ramps, the landscape of urban mobility is changing.\n\nIn London, the 'Step-Free' Tube map is an essential tool. However, even with the map, lift outages can happen. We recommend checking the TfL status updates and using community feedback on AccessAdvisr to see how reliable the access really is in real-time.",
                "excerpt": "Getting from one place to another should be easy for everyone. Discover the latest in accessible transport."
            },
            {
                "title": "Accessible Shopping Tips for a Smooth Experience",
                "category": "Community Stories",
                "content": "Finding the right stores and making your shopping trip easy can be challenging if you need accessible shopping. Everyone deserves a smooth experience where aisles are wide enough and fitting rooms are actually accessible.\n\nMany flagship stores in London now offer 'quiet hours' for shoppers with autism. Additionally, many retail complexes have improved their Changing Places facilities. Share your shopping wins and frustrations with us to help others plan their trips better!",
                "excerpt": "Finding the right stores and making your shopping trip easy can be challenging. Here's how to navigate the high street."
            }
        ]

        for data in posts_data:
            cat = next(c for c in cat_objs if c.name == data["category"])
            post, created = BlogPost.objects.get_or_create(
                title=data["title"],
                defaults={
                    'slug': slugify(data["title"]),
                    'category': cat,
                    'author': author,
                    'content': data["content"],
                    'excerpt': data["excerpt"],
                    'is_published': True
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created post: {data['title']}"))

        self.stdout.write(self.style.SUCCESS("Blog seeding complete!"))
