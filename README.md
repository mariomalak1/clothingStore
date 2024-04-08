# clothingStore

This Project is for managing a series of stores or brands, any user can make orders to customers.
manager user has access to everything as admin but, in his branch only.
except he can't access any branch else his
admin user can see all branches sales and some statistics for sales in branches, and a lot of features

Some features:

- create the invoice pdf and print it 
- edit product in a specific branch -> for admin can edit anything, for manager can edit quantity and price only
- if user deleted, all of his created products and orders will be moved to the admin who deleted him
- admin can change user permission for any user at any time --> except the other admins
- superuser --> super admin --> appears as a normal admin, but he can go to admins pages and edit admins also as he wants
- Search in all carts with number of orders
- if product quantity in a branch is equal to 0 will not appear in "create order form"
- display all users
- if cart will be cancelled and no orders in it, delete it without go to delete page
- if press order and not chosen a specific product, display message not error
- admin can suspend any user except the other admins 

to run this program on your machine 



To run this program on your machine:

First, you want to install only Python programming language from https://www.python.org/

**Remember**: To Add Python To Path in the Installation

32-bit version:

https://www.python.org/ftp/python/3.10.10/python-3.10.10.exe

64-bit version:

https://www.python.org/ftp/python/3.10.10/python-3.10.10-amd64.exe


then open cmd and run this command

```shell
pip install -r requirements.txt
py manage.py migrate
py manage.py runserver
```

