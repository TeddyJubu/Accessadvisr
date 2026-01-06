What is it:
AccessAdvisr is an accessibility review platform for places worldwide.

It lets disabled people and allies share and read user-led accessibility reviews of venues—covering categories like Accommodation, Entertainment, Food & Drink, Shopping, Sports & Recreational, Transport, and Travel & Tour. Listings show location, contact, price ranges, ratings, and status (open/closed), and the site highlights most-rated places and recent contributions. You can also add listings, post reviews, browse categories, and follow community updates and blogs. In short, it’s a community-driven guide to help plan visits with confidence, where accessibility comes first.

A concise way to describe it:
“AccessAdvisr is a community-powered directory of accessibility reviews for places around the world, helping disabled travellers discover, evaluate, and share real-world access information.”

Plan

1. Scaffold Django project and app, configure templates/static.

2. Create Home and Admin pages using your HTML and a simple admin scaffold.

3. Add base layout with header nav buttons for Public and Admin; include Tailwind CDN and lucide.

4. Break large homepage into partials iteratively.

5. Prepare for future data models and server-side rendering; leave auth for later.

Instructions for the AI

1. Create project and app

- Run:

 ▫ django-admin startproject accessadvisr

 ▫ cd accessadvisr

 ▫ python manage.py startapp core

- In accessadvisr/settings.py:

 ▫ Add ‘core’ to INSTALLED_APPS.

 ▫ Set TEMPLATES DIRS:

 ⁃ ‘DIRS’: [BASE_DIR / ‘templates’]

 ▫ Set STATIC_URL = ‘/static/’

 ▫ Add STATICFILES_DIRS = [BASE_DIR / ‘static’]

- Create folders:

 ▫ templates/

 ▫ templates/core/

 ▫ static/

2. Base layout and routing

- In templates/base.html add the global header and Tailwind CDN and lucide CDN:

<!-- templates/base.html -->

<!DOCTYPE html>

<html lang="en">

<head>

  <meta charset="utf-8" />

  <meta name="viewport" content="width=device-width, initial-scale=1" />

  <title>{% block title %}AccessAdvisr{% endblock %}</title>

  <script src="https://cdn.tailwindcss.com"></script>

  <script src="https://unpkg.com/lucide@latest"></script>

</head>

<body class="bg-white text-slate-700 antialiased font-sans">

  <header class="bg-white border-b border-gray-100 sticky top-0 z-50">

    <div class="container mx-auto px-4 h-20 flex items-center justify-between">

      <a href="{% url 'home' %}" class="flex items-center gap-2">

        <img src="https://accessadvisr.com/wp-content/uploads/2020/02/accessAdvisr_logo.jpeg" alt="AccessAdvisr" class="h-10 w-auto">

      </a>

      <nav class="hidden lg:flex items-center gap-6 text-sm font-semibold text-slate-600">

        <a href="{% url 'home' %}" class="hover:text-[#FF431E]">Public</a>

        <a href="{% url 'admin_page' %}" class="hover:text-[#FF431E]">Admin</a>

      </nav>

      <button class="lg:hidden text-slate-600" id="mobile-menu-button" aria-controls="mobile-menu" aria-expanded="false">

        <i data-lucide="menu" class="w-6 h-6"></i>

      </button>

    </div>

  </header>

  <div id="mobile-menu" class="lg:hidden fixed inset-0 bg-white/95 backdrop-blur-sm hidden" role="dialog" aria-modal="true">

    <nav class="p-6 space-y-4 text-slate-700">

      <a href="{% url 'home' %}" class="block font-semibold">Public</a>

      <a href="{% url 'admin_page' %}" class="block font-semibold">Admin</a>

      <button id="mobile-close" class="mt-6 w-full bg-[#FF431E] text-white py-3 rounded font-bold">Close</button>

    </nav>

  </div>

  <main>

    {% block content %}{% endblock %}

  </main>

  <script>

    lucide.createIcons();

    const menuBtn = document.getElementById('mobile-menu-button');

    const mobileMenu = document.getElementById('mobile-menu');

    const mobileClose = document.getElementById('mobile-close');

    function openMenu(){ mobileMenu.classList.remove('hidden'); menuBtn.setAttribute('aria-expanded','true'); }

    function closeMenu(){ mobileMenu.classList.add('hidden'); menuBtn.setAttribute('aria-expanded','false'); }

    if(menuBtn){ menuBtn.addEventListener('click', openMenu); }

    if(mobileClose){ mobileClose.addEventListener('click', closeMenu); }

    mobileMenu?.addEventListener('click', (e)=>{ if(e.target===mobileMenu) closeMenu(); });

  </script>

</body>

</html>

- Create core/urls.py and wire routes:

# core/urls.py

from django.urls import path

from . import views

urlpatterns = [

    path('', views.home, name='home'),

    path('admin-page/', views.admin_page, name='admin_page'),

]

- Update accessadvisr/urls.py to include core URLs:

# accessadvisr/urls.py

from django.contrib import admin

from django.urls import path, include

urlpatterns = [

    path('dj-admin/', admin.site.urls),  # Django's built-in admin

    path('', include('core.urls')),

]

3. Home page template using your HTML

- Place your provided HTML into templates/core/home.html, wrapped with base.html and split into blocks. Keep Tailwind CDN and lucide only in base.html. Replace only the outer   <html>,   <head>,   <body> with extends.

<!-- templates/core/home.html -->

{% extends "base.html" %}

{% block title %}AccessAdvisr — Home{% endblock %}

{% block content %}

<!-- Paste your homepage HTML sections here except the outer html/head/body and header -->

<!-- Example: Map Hero, Search Bar, Explore, Stats, Contributions, Testimonial, Footer, Back to top -->

<!-- Keep your scripts at the bottom of this block, but remove lucide.createIcons() (already in base) -->

<section class="relative w-full h-[600px] bg-slate-100 overflow-hidden group">

  <!-- ... your map hero HTML ... -->

</section>

<div class="container mx-auto px-4 relative -mt-10 z-20 mb-20">

  <!-- ... your search bar HTML ... -->

</div>

<section class="container mx-auto px-4 py-16">

  <!-- ... Explore section (3 cards) ... -->

</section>

<section class="relative py-20 bg-orange-500 overflow-hidden">

  <!-- ... Stats section ... -->

</section>

<section class="container mx-auto px-4 py-20">

  <!-- ... Most Recent Contributions ... -->

</section>

<section class="relative py-24 bg-cover bg-center bg-fixed" style="background-image: url('https://accessadvisr.com/wp-content/uploads/2020/02/c4-2.jpg');">

  <!-- ... Testimonial Slider ... -->

</section>

<footer class="bg-[#26354E] text-gray-400 py-16 text-sm">

  <!-- ... Footer ... -->

</footer>

<a href="#" class="fixed bottom-8 right-8 bg-[#26354E] hover:bg-[#FF431E] text-white w-10 h-10 flex items-center justify-center rounded shadow-lg transition-colors z-50" id="back-to-top" aria-label="Back to top">

  <i data-lucide="arrow-up" class="w-5 h-5"></i>

</a>

<script>

// Smooth scroll back to top with reduced motion

const backToTop = document.getElementById('back-to-top');

const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

backToTop?.addEventListener('click', (e) => {

  e.preventDefault();

  window.scrollTo({ top: 0, behavior: prefersReduced ? 'auto' : 'smooth' });

});

// Stats counters: use unique IDs and intersection observer

function animateCounter(el){

  const target = parseInt(el.getAttribute('data-target'),10);

  const duration = 2000, stepTime = 20;

  const steps = Math.floor(duration/stepTime);

  let current = 0, inc = target/steps;

  const t = setInterval(()=>{

    current += inc;

    if(current >= target){ el.textContent = target + "+"; clearInterval(t); }

    else { el.textContent = Math.floor(current) + "+"; }

  }, stepTime);

}

const counters = Array.from(document.querySelectorAll('[data-target]'));

const obs = new IntersectionObserver((entries,o)=>{

  entries.forEach(entry=>{

    if(entry.isIntersecting){ animateCounter(entry.target); o.unobserve(entry.target); }

  });

},{threshold:0.5});

counters.forEach(c=>obs.observe(c));

</script>

{% endblock %}

4. Minimal Admin page (publicly accessible, auth later)

- Create templates/core/admin.html:

<!-- templates/core/admin.html -->

{% extends "base.html" %}

{% block title %}AccessAdvisr — Admin{% endblock %}

{% block content %}

<section class="container mx-auto px-4 py-12">

  <h1 class="text-2xl font-bold text-[#26354E] mb-6">Admin Dashboard (Preview)</h1>

  <p class="text-slate-600 mb-8">Authentication will be added later. This page is public for now.</p>

  <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">

    <div class="bg-white border border-gray-200 rounded p-6">

      <h2 class="font-semibold mb-4">Seed Sample Data</h2>

      <form method="post" action="">

        {% csrf_token %}

        <button class="bg-[#FF431E] hover:bg-[#e03615] text-white px-4 py-2 rounded font-bold">Seed Listings</button>

      </form>

    </div>

    <div class="bg-white border border-gray-200 rounded p-6">

      <h2 class="font-semibold mb-4">Current Listings (Mock)</h2>

      <ul class="space-y-2">

        <li class="flex justify-between"><span>Exbury Gardens & Steam Railway</span><span class="text-slate-500">$60–$85 • 4.0 • Open</span></li>

        <li class="flex justify-between"><span>Hotel Sercotel La Boroña</span><span class="text-slate-500">$100–$120 • 4.5 • Open</span></li>

        <li class="flex justify-between"><span>Swansea.com Stadium</span><span class="text-slate-500">$20–$50 • 4.1 • Open</span></li>

      </ul>

    </div>

  </div>

</section>

{% endblock %}

5. Views

- Implement simple views that render templates and handle the seed POST stub. Keep data in-memory for now.

# core/views.py

from django.shortcuts import render, redirect

from django.views.decorators.http import require_http_methods

def home(request):

    return render(request, "core/home.html")

@require_http_methods(["GET", "POST"])

def admin_page(request):

    if request.method == "POST":

        # TODO: in future, seed DB; for now just redirect with a flash message stub

        return redirect("admin_page")

    return render(request, "core/admin.html")

6. Iterative design enhancements (next passes)

- Split home sections into partials:

 ▫ templates/core/partials/search_bar.html

 ▫ templates/core/partials/explore_cards.html

 ▫ templates/core/partials/stats.html

 ▫ templates/core/partials/contributions.html

- Include with ‎⁠{% include "core/partials/search_bar.html" %}⁠ from home.html to keep templates maintainable.


- Accessibility:

 ▫ Ensure buttons have aria-labels where icon-only.

 ▫ Use focus-visible rings via Tailwind: focus:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-orange-500.

7. Suggested future stack for persistence and auth (do not implement now)

- Database: PostgreSQL

- ORM: Django ORM (built-in)

- Auth: django-allauth or Django’s built-in auth, with email login; gate /admin-page later

- Storage: S3-compatible for images

- Deployment: Render/Sevalla/Heroku or any Django-friendly host

- Admin CMS: Django admin for internal data management

Run server

- python manage.py migrate

- python manage.py runserver

- Visit http://127.0.0.1:8000/ for Public and http://127.0.0.1:8000/admin-page/ for Admin preview

Security notes

- Keep /admin-page public for now per plan; do not expose real data or credentials.

- When enabling auth, restrict actions and protect seed operations with CSRF (already included) and permissions.

---
Here are Django template partials for your homepage, with includes wired into a clean base layout. Paste these files into your Django project as shown.

1. templates/base.html
A shared layout with header nav buttons to Public and Admin, Tailwind CDN, lucide, and mobile menu.

<!-- templates/base.html -->

<!DOCTYPE html>

<html lang="en">

<head>

  <meta charset="utf-8" />

  <meta name="viewport" content="width=device-width, initial-scale=1" />

  <title>{% block title %}AccessAdvisr{% endblock %}</title>

  <script src="https://cdn.tailwindcss.com"></script>

  <script src="https://unpkg.com/lucide@latest"></script>

</head>

<body class="bg-white text-slate-700 antialiased font-manrope">

  <header class="bg-white border-b border-gray-100 sticky top-0 z-50">

    <div class="container mx-auto px-4 h-20 flex items-center justify-between">

      <a href="{% url 'home' %}" class="flex items-center gap-2">

        <img src="https://accessadvisr.com/wp-content/uploads/2020/02/accessAdvisr_logo.jpeg" alt="AccessAdvisr" class="h-10 w-auto">

      </a>

      <nav class="hidden lg:flex items-center gap-8 text-sm font-semibold text-slate-600">

        <a href="{% url 'home' %}" class="hover:text-[#FF431E]">Public</a>

        <a href="{% url 'admin_page' %}" class="hover:text-[#FF431E]">Admin</a>

      </nav>

      <button class="lg:hidden text-slate-600" id="mobile-menu-button" aria-controls="mobile-menu" aria-expanded="false">

        <i data-lucide="menu" class="w-6 h-6"></i>

      </button>

    </div>

  </header>

  <!-- Mobile Menu -->

  <div id="mobile-menu" class="lg:hidden fixed inset-0 bg-white/95 backdrop-blur-sm hidden" role="dialog" aria-modal="true">

    <nav class="p-6 space-y-4 text-slate-700">

      <a href="{% url 'home' %}" class="block font-semibold">Public</a>

      <a href="{% url 'admin_page' %}" class="block font-semibold">Admin</a>

      <button id="mobile-close" class="mt-6 w-full bg-[#FF431E] text-white py-3 rounded font-bold">Close</button>

    </nav>

  </div>

  <main>

    {% block content %}{% endblock %}

  </main>

  <script>

    lucide.createIcons();

    const menuBtn = document.getElementById('mobile-menu-button');

    const mobileMenu = document.getElementById('mobile-menu');

    const mobileClose = document.getElementById('mobile-close');

    function openMenu(){ mobileMenu.classList.remove('hidden'); menuBtn.setAttribute('aria-expanded','true'); }

    function closeMenu(){ mobileMenu.classList.add('hidden'); menuBtn.setAttribute('aria-expanded','false'); }

    menuBtn?.addEventListener('click', openMenu);

    mobileClose?.addEventListener('click', closeMenu);

    mobileMenu?.addEventListener('click', (e)=>{ if(e.target===mobileMenu) closeMenu(); });

  </script>

</body>

</html>

2. templates/core/home.html
The homepage composed from partials.

<!-- templates/core/home.html -->

{% extends "base.html" %}

{% block title %}AccessAdvisr — Home{% endblock %}

{% block content %}

{% include "core/partials/hero_map.html" %}

{% include "core/partials/search_bar.html" %}

{% include "core/partials/explore_cards.html" %}

{% include "core/partials/stats.html" %}

{% include "core/partials/contributions.html" %}

{% include "core/partials/testimonial.html" %}

{% include "core/partials/footer.html" %}

{% include "core/partials/back_to_top.html" %}

{% include "core/partials/scripts.html" %}

{% endblock %}

3. Partial files
Create a folder templates/core/partials/ and add the following.

hero_map.html<!-- templates/core/partials/hero_map.html -->

<section class="relative w-full h-[600px] bg-slate-100 overflow-hidden group">

  <div class="absolute inset-0 bg-cover bg-center" style="background-image: url('https://upload.wikimedia.org/wikipedia/commons/e/ec/Map_of_New_York_City_location_map.jpg'); opacity: 0.8;"></div>

  <div class="absolute inset-0 bg-white/10 pointer-events-none"></div>

  <!-- Fake Markers -->

  <div class="absolute top-1/3 left-1/4 -translate-x-1/2 -translate-y-1/2">

    <div class="relative">

      <div class="w-12 h-12 bg-[#FF431E] rounded-full border-4 border-white shadow-lg flex items-center justify-center text-white font-bold">3</div>

      <div class="w-4 h-4 bg-[#FF431E] absolute -bottom-1 left-1/2 -translate-x-1/2 rotate-45"></div>

    </div>

  </div>

  <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2">

    <div class="relative">

      <div class="w-12 h-12 overflow-hidden rounded-full border-4 border-white shadow-lg">

        <img src="https://accessadvisr.com/wp-content/uploads/2020/01/user-1-150x150.png" class="w-full h-full object-cover" alt="">

      </div>

      <div class="w-4 h-4 bg-white absolute -bottom-1 left-1/2 -translate-x-1/2 rotate-45"></div>

    </div>

  </div>

  <div class="absolute bottom-1/3 right-1/4 -translate-x-1/2 -translate-y-1/2">

    <div class="w-10 h-10 bg-[#26354E] rounded-full border-4 border-white shadow-lg flex items-center justify-center text-white font-bold text-xs">2</div>

  </div>

  <!-- Controls (placeholders) -->

  <div class="absolute top-4 left-4 flex flex-col gap-2">

    <button class="bg-white p-2 rounded shadow hover:bg-gray-50 text-slate-600" aria-disabled="true" title="Map zoom controls are placeholders">

      <i data-lucide="plus" class="w-4 h-4"></i>

    </button>

    <button class="bg-white p-2 rounded shadow hover:bg-gray-50 text-slate-600" aria-disabled="true" title="Map zoom controls are placeholders">

      <i data-lucide="minus" class="w-4 h-4"></i>

    </button>

  </div>

</section>

search_bar.html<!-- templates/core/partials/search_bar.html -->

<div class="container mx-auto px-4 relative -mt-10 z-20 mb-20">

  <div class="bg-white p-6 rounded shadow-xl grid grid-cols-1 md:grid-cols-4 gap-4 items-center border border-gray-100">

    <div class="flex items-center gap-3 border-b md:border-b-0 md:border-r border-gray-200 pb-4 md:pb-0 px-2">

      <i data-lucide="edit-3" class="w-5 h-5 text-gray-400"></i>

      <input type="text" placeholder="Keywords..." class="w-full outline-none text-slate-600 placeholder-gray-400" aria-label="Keywords">

    </div>

    <div class="flex items-center gap-3 border-b md:border-b-0 md:border-r border-gray-200 pb-4 md:pb-0 px-2">

      <i data-lucide="layers" class="w-5 h-5 text-gray-400"></i>

      <select class="w-full outline-none text-slate-600 bg-transparent cursor-pointer" aria-label="Filter by category">

        <option>Filter by category</option>

        <option>Accommodation</option>

        <option>Food &amp; Drink</option>

      </select>

    </div>

    <div class="flex items-center gap-3 border-b md:border-b-0 md:border-r border-gray-200 pb-4 md:pb-0 px-2">

      <i data-lucide="map-pin" class="w-5 h-5 text-gray-400"></i>

      <input type="text" placeholder="Location" class="w-full outline-none text-slate-600 placeholder-gray-400" aria-label="Location">

    </div>

    <div>

      <button class="w-full bg-[#FF431E] hover:bg-[#e03615] text-white py-3 px-6 rounded font-bold transition-colors shadow-lg shadow-orange-200">

        Search

      </button>

    </div>

  </div>

</div>

explore_cards.html<!-- templates/core/partials/explore_cards.html -->

<section class="container mx-auto px-4 py-16">

  <div class="text-center mb-12">

    <h2 class="text-3xl font-bold text-[#26354E] mb-4 tracking-tight">Explore Most Rated <span class="text-[#FF431E]">Places</span></h2>

    <p class="text-slate-500 max-w-2xl mx-auto">Discover the most rated places reviewed by our community.</p>

  </div>

  <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">

    {% comment %} Card 1 {% endcomment %}

    <div class="bg-white rounded-lg shadow-sm border border-gray-100 overflow-hidden group hover:shadow-xl transition-shadow duration-300">

      <div class="relative h-60 overflow-hidden">

        <img src="https://accessadvisr.com/wp-content/uploads/2020/01/exbury-gardens-steam-railway-540x300.jpg" alt="Exbury Gardens" class="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110">

        <div class="absolute top-4 left-4 bg-black/60 text-white text-xs font-semibold px-3 py-1 rounded-sm">$60 - $85</div>

        <div class="absolute bottom-4 left-4 bg-[#FF431E] text-white text-xs font-semibold px-2 py-1 rounded-sm">4.0</div>

        <button class="absolute top-4 right-4 bg-black/40 hover:bg-[#FF431E] text-white p-2 rounded-full transition-colors" aria-label="Save">

          <i data-lucide="heart" class="w-4 h-4"></i>

        </button>

      </div>

      <div class="p-6 relative">

        <div class="absolute -top-8 right-6">

          <img src="https://accessadvisr.com/wp-content/uploads/2020/01/user-3-150x150.jpg" class="w-16 h-16 rounded-full border-4 border-white shadow-md" alt="">

        </div>

        <h3 class="text-lg font-bold text-[#26354E] mb-1 hover:text-[#FF431E] cursor-pointer">Exbury Gardens &amp; Steam Railway</h3>

        <p class="text-xs text-slate-400 mb-4">Villa, food for you</p>

        <div class="flex items-center gap-1 text-slate-500 text-sm mb-2">

          <i data-lucide="map-pin" class="w-4 h-4 text-gray-400"></i> New York, USA

        </div>

        <div class="flex items-center gap-1 text-slate-500 text-sm mb-4">

          <i data-lucide="phone" class="w-4 h-4 text-gray-400"></i> +88-123-456-789

        </div>

        <div class="border-t border-gray-100 pt-4 flex items-center justify-between mt-4">

          <div class="flex items-center gap-2">

            <span class="bg-gray-100 text-slate-600 text-xs px-2 py-1 rounded">Food &amp; Restaurants</span>

            <span class="bg-gray-100 text-slate-400 text-xs px-2 py-1 rounded">+1</span>

          </div>

          <span class="text-[#FF431E] text-sm font-semibold">Open</span>

        </div>

      </div>

    </div>

    {% comment %} Card 2 {% endcomment %}

    <div class="bg-white rounded-lg shadow-sm border border-gray-100 overflow-hidden group hover:shadow-xl transition-shadow duration-300">

      <div class="relative h-60 overflow-hidden">

        <img src="https://accessadvisr.com/wp-content/uploads/2020/01/Hotel-Sercotel-La-Borona-540x300.jpg" alt="Hotel Sercotel" class="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110">

        <div class="absolute top-4 left-4 bg-black/60 text-white text-xs font-semibold px-3 py-1 rounded-sm">$100 - $120</div>

        <div class="absolute bottom-4 left-4 bg-[#FF431E] text-white text-xs font-semibold px-2 py-1 rounded-sm">4.5</div>

        <button class="absolute top-4 right-4 bg-black/40 hover:bg-[#FF431E] text-white p-2 rounded-full transition-colors" aria-label="Save">

          <i data-lucide="heart" class="w-4 h-4"></i>

        </button>

      </div>

      <div class="p-6 relative">

        <div class="absolute -top-8 right-6">

          <img src="https://accessadvisr.com/wp-content/uploads/2020/01/user-2-150x150.jpg" class="w-16 h-16 rounded-full border-4 border-white shadow-md" alt="">

        </div>

        <h3 class="text-lg font-bold text-[#26354E] mb-1 hover:text-[#FF431E] cursor-pointer flex items-center gap-2">

          Hotel Sercotel La Boroña

          <span class="bg-green-500 text-white rounded-full p-0.5"><i data-lucide="check" class="w-2 h-2"></i></span>

        </h3>

        <p class="text-xs text-slate-400 mb-4">Outdoor, luxury for you</p>

        <div class="flex items-center gap-1 text-slate-500 text-sm mb-2">

          <i data-lucide="map-pin" class="w-4 h-4 text-gray-400"></i> New York, USA

        </div>

        <div class="flex items-center gap-1 text-slate-500 text-sm mb-4">

          <i data-lucide="phone" class="w-4 h-4 text-gray-400"></i> +89-456-888-666

        </div>

        <div class="border-t border-gray-100 pt-4 flex items-center justify-between mt-4">

          <div class="flex items-center gap-2">

            <span class="bg-gray-100 text-slate-600 text-xs px-2 py-1 rounded">Education</span>

            <span class="bg-gray-100 text-slate-400 text-xs px-2 py-1 rounded">+2</span>

          </div>

          <span class="text-[#FF431E] text-sm font-semibold">Open</span>

        </div>

      </div>

    </div>

    {% comment %} Card 3 {% endcomment %}

    <div class="bg-white rounded-lg shadow-sm border border-gray-100 overflow-hidden group hover:shadow-xl transition-shadow duration-300">

      <div class="relative h-60 overflow-hidden">

        <img src="https://accessadvisr.com/wp-content/uploads/2020/01/swansea.com-stadium-540x300.jpg" alt="Swansea Stadium" class="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110">

        <div class="absolute top-4 left-4 bg-black/60 text-white text-xs font-semibold px-3 py-1 rounded-sm">$20 - $50</div>

        <div class="absolute bottom-4 left-4 bg-[#FF431E] text-white text-xs font-semibold px-2 py-1 rounded-sm">4.1</div>

        <button class="absolute top-4 right-4 bg-black/40 hover:bg-[#FF431E] text-white p-2 rounded-full transition-colors" aria-label="Save">

          <i data-lucide="heart" class="w-4 h-4"></i>

        </button>

      </div>

      <div class="p-6 relative">

        <div class="absolute -top-8 right-6">

          <img src="https://accessadvisr.com/wp-content/uploads/2020/01/user-1-150x150.png" class="w-16 h-16 rounded-full border-4 border-white shadow-md bg-white" alt="">

        </div>

        <h3 class="text-lg font-bold text-[#26354E] mb-1 hover:text-[#FF431E] cursor-pointer flex items-center gap-2">

          Swansea.com Stadium

          <span class="bg-green-500 text-white rounded-full p-0.5"><i data-lucide="check" class="w-2 h-2"></i></span>

        </h3>

        <p class="text-xs text-slate-400 mb-4">Active for you, my friend</p>

        <div class="flex items-center gap-1 text-slate-500 text-sm mb-2">

          <i data-lucide="map-pin" class="w-4 h-4 text-gray-400"></i> New York, USA

        </div>

        <div class="flex items-center gap-1 text-slate-500 text-sm mb-4">

          <i data-lucide="phone" class="w-4 h-4 text-gray-400"></i> +89-123-456-789

        </div>

        <div class="border-t border-gray-100 pt-4 flex items-center justify-between mt-4">

          <div class="flex items-center gap-2">

            <span class="bg-gray-100 text-slate-600 text-xs px-2 py-1 rounded">Sport</span>

          </div>

          <span class="text-[#FF431E] text-sm font-semibold">Open</span>

        </div>

      </div>

    </div>

  </div>

</section>

stats.html<!-- templates/core/partials/stats.html -->

<section class="relative py-20 bg-orange-500 overflow-hidden">

  <div class="absolute inset-0 bg-gradient-to-r from-orange-500 to-red-500 opacity-90"></div>

  <div class="absolute inset-0 bg-cover bg-center" style="background-image: url('https://accessadvisr.com/wp-content/uploads/2025/11/Award-Winning-Section.jpg'); opacity: 0.1;"></div>

  <div class="container mx-auto px-4 relative z-10">

    <div class="grid grid-cols-2 md:grid-cols-4 gap-8 text-center text-white">

      <div class="flex flex-col items-center">

        <div class="mb-4 p-4 border-2 border-white/30 rounded-full">

          <i data-lucide="trophy" class="w-8 h-8"></i>

        </div>

        <div id="awards-counter" class="text-4xl font-extrabold mb-1" data-target="200">0+</div>

        <div class="text-sm font-semibold uppercase tracking-wide opacity-90">Awards Winning</div>

      </div>

      <div class="flex flex-col items-center">

        <div class="mb-4 p-4 border-2 border-white/30 rounded-full">

          <i data-lucide="briefcase" class="w-8 h-8"></i>

        </div>

        <div id="projects-counter" class="text-4xl font-extrabold mb-1" data-target="307">0+</div>

        <div class="text-sm font-semibold uppercase tracking-wide opacity-90">Done Projects</div>

      </div>

      <div class="flex flex-col items-center">

        <div class="mb-4 p-4 border-2 border-white/30 rounded-full">

          <i data-lucide="smile" class="w-8 h-8"></i>

        </div>

        <div id="clients-counter" class="text-4xl font-extrabold mb-1" data-target="700">0+</div>

        <div class="text-sm font-semibold uppercase tracking-wide opacity-90">Happy Clients</div>

      </div>

      <div class="flex flex-col items-center">

        <div class="mb-4 p-4 border-2 border-white/30 rounded-full">

          <i data-lucide="coffee" class="w-8 h-8"></i>

        </div>

        <div id="coffee-counter" class="text-4xl font-extrabold mb-1" data-target="770">0+</div>

        <div class="text-sm font-semibold uppercase tracking-wide opacity-90">Cups Of Coffee</div>

      </div>

    </div>

  </div>

</section>

contributions.html<!-- templates/core/partials/contributions.html -->

<section class="container mx-auto px-4 py-20">

  <div class="text-center mb-12">

    <h2 class="text-4xl font-bold text-[#26354E] mb-4 tracking-tight">Most Recent <span class="text-[#FF431E]">Contributions</span></h2>

    <p class="text-slate-500 max-w-4xl mx-auto text-base">Check Out The Most Recent Contributions From Our Members.</p>

  </div>

  <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">

    <!-- Review 1 -->

    <div class="bg-white rounded-lg border border-gray-200 overflow-hidden flex flex-col shadow-sm">

      <div class="p-6 flex items-center gap-4">

        <img src="https://accessadvisr.com/wp-content/uploads/2025/11/thumb-Screenshot_20240725_174546_Facebook.jpg" class="w-16 h-16 rounded-full object-cover" alt="">

        <div>

          <h4 class="font-bold text-[#26354E] text-lg">ecologisttobe</h4>

          <div class="flex gap-1 mt-1 text-[#FFC107]">

            {% for i in "12345" %}

              <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="currentColor" class="w-4 h-4"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>

            {% endfor %}

          </div>

        </div>

      </div>

      <div class="bg-[#FF431E] p-8 text-white text-sm font-medium leading-relaxed flex-grow flex items-center">

        ecologisttobe reviewed Vaillant Live, 2 Colyear St, Derby DE1 1LA

      </div>

    </div>

    <!-- Review 2 -->

    <div class="bg-white rounded-lg border border-gray-200 overflow-hidden flex flex-col shadow-sm">

      <div class="p-6 flex items-center gap-4">

        <img src="https://accessadvisr.com/wp-content/uploads/2025/11/thumb-20.jpg" class="w-16 h-16 rounded-full object-cover" alt="">

        <div>

          <h4 class="font-bold text-[#26354E] text-lg">Rob Trent</h4>

          <div class="flex gap-1 mt-1">

            {% for i in "123" %}

              <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="#FFC107" class="w-4 h-4"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>

            {% endfor %}

            {% for i in "45" %}

              <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="#E5E7EB" class="w-4 h-4"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>

            {% endfor %}

          </div>

        </div>

      </div>

      <div class="bg-[#FF431E] p-8 text-white text-sm font-medium leading-relaxed flex-grow flex items-center">

        Rob Trent reviewed Boathouse Swanwick, Swanwick Marina, Swanwick Shore Rd

      </div>

    </div>

    <!-- Review 3 -->

    <div class="bg-white rounded-lg border border-gray-200 overflow-hidden flex flex-col shadow-sm">

      <div class="p-6 flex items-center gap-4">

        <img src="https://accessadvisr.com/wp-content/uploads/2025/11/thumb-IMG_5760-rotated.jpeg" class="w-16 h-16 rounded-full object-cover" alt="">

        <div>

          <h4 class="font-bold text-[#26354E] text-lg">Matt</h4>

          <div class="flex gap-1 mt-1 text-[#FFC107]">

            {% for i in "12345" %}

              <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="currentColor" class="w-4 h-4"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>

            {% endfor %}

          </div>

        </div>

      </div>

      <div class="bg-[#FF431E] p-8 text-white text-sm font-medium leading-relaxed flex-grow flex items-center">

        Matt rated Premier Inn London Wembley Park hotel, 151 Wembley Park Dr, Wembley Park

      </div>

    </div>

  </div>

  <div class="text-center mt-12">

    <button class="bg-[#FF431E] hover:bg-[#d63515] text-white py-3 px-10 rounded font-bold text-sm transition-colors shadow-sm">

      See All

    </button>

  </div>

</section>

testimonial.html<!-- templates/core/partials/testimonial.html -->

<section class="relative py-24 bg-cover bg-center bg-fixed" style="background-image: url('https://accessadvisr.com/wp-content/uploads/2020/02/c4-2.jpg');">

  <div class="absolute inset-0 bg-[#26354E]/80"></div>

  <div class="container mx-auto px-4 relative z-10 text-center">

    <div class="max-w-3xl mx-auto">

      <div class="mb-8">

        

