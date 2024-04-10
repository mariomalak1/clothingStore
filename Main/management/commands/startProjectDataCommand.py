from django.core.management.base import BaseCommand
from Seller import models as SellerModel
from Main import models as MainModels

class Command(BaseCommand):
    def handle(self, *args, **options):
        print("welcome in mario clothing store project.")

        # create branch, after while he can enter website and change it
        branch = SellerModel.Branch(name="branch 1")
        branch.save()

        # create site user to be an admin and can open the admin pages
        user_ = SellerModel.Site_User(username="admin1", branch=branch, user_type=0)
        user_.set_password("password1")
        user_.save()

        print("done starter data.")
        print("you now can enter website with username = 'admin1'\nand password = 'password1'\nand you have already created branch called 'branch 1'")
