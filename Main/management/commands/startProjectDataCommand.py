from django.core.management.base import BaseCommand
from Seller import models as SellerModel
from Main import models as MainModels

class Command(BaseCommand):
    def handle(self, *args, **options):
        print("welcome in mario clothing store project.")

        # create branch, after while he can enter website and change it
        try:
            branch = SellerModel.Branch(name="branch 1")
            branch.save()
            print("branch with name 'branch 1' added successfully, you can enter website and change it")
        except:
            branch = SellerModel.Branch.objects.first()
            print("branch with name 'branch 1' is already exist, no need to create dummy data!.")
        try:
            # create site user to be an admin and can open the admin pages
            user_ = SellerModel.Site_User(username="admin1", branch=branch, user_type=0)
            user_.set_password("password1")
            user_.save()
        except:
            user_ = SellerModel.Site_User.objects.filter(username="admin1").first()
            user_.set_password("password2")
            user_.save()
            print("username is already exist and will change this password to : password2")

        site = MainModels.SiteSettings.objects.first()
        if not site:
            site = MainModels.SiteSettings(SiteName="Mario Site")
            site.save()

        print("done starter data.")