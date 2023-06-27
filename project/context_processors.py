# context_processors.py
from Main.models import SiteSettings
from Seller.models import Site_User
from django.shortcuts import get_object_or_404
def get_site_name(request):
    # Retrieve the dynamic data from the database
    site_name = SiteSettings.objects.all().first()  # Example: fetching all objects from YourModel
    try:
        user_site = get_object_or_404(Site_User, id = request.user.id)
    except:
        user_site = None
    # Return the data as a dictionary
    return {
        'site_name': site_name.SiteName,
        "user_site":user_site,
    }
