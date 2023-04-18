from django.shortcuts import render

# Create your views here.

def home_page(request):
    return render(request, "Main/home_page.html")

def admin_panel(request):
    return render(request, "Main/admin_panel.html")