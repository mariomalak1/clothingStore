import pdfkit
import io
import base64
import os
from project.settings import BASE_DIR
from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponse
from django.template.loader import render_to_string
from django.templatetags.static import static

from Invoice.models import Cart
from Seller.models import Site_User
# create views here.


def create_invoice(request, cart_code):
    cart_ = Cart.objects.filter(cart_code=cart_code).first()
    current_user = get_object_or_404(Site_User, id=request.user.id)
    if cart_:
        # to put logo on
        logo_path = os.path.join(BASE_DIR, 'static/Logo', 'MarioLogo.png')
        with open(logo_path, 'rb') as logo_file:
            logo_data = base64.b64encode(logo_file.read()).decode('utf-8')

        context = {
            "cart":cart_,
            "current_user":current_user,
            "logo_data":logo_data,
        }

        template = render(request, "Invoice/invoice.html", context)
        html_content = template.content.decode('utf-8')
        path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
        config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
        options = {
            'dpi': 365,
            'page-size': 'A4',
            'margin-top': '0in',
            'margin-right': '0in',
            'margin-bottom': '0in',
            'margin-left': '0in',
            'custom-header': [
                ('Accept-Encoding', 'gzip')
            ],
            'no-outline': None,
            "enable-local-file-access": "",
        }
        pdf = pdfkit.from_string(html_content, options=options, configuration=config)
        # Create the HttpResponse object with the PDF content
        response = HttpResponse(pdf, content_type='application/pdf')

        # Set the Content-Disposition header to force a download
        response['Content-Disposition'] = f'attachment; filename="{cart_.cart_code}.pdf"'
        return response
    else:
        return Http404()