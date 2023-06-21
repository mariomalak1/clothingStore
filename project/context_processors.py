# context_processors.py
from Main.models import SiteSettings

def get_site_name(request):
    # Retrieve the dynamic data from the database
    site_name = SiteSettings.objects.all().first()  # Example: fetching all objects from YourModel

    # Return the data as a dictionary
    return {
        'site_name': site_name.SiteName,
    }
