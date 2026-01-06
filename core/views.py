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
