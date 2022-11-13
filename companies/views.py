import os
from django.core import mail
from django.template.loader import render_to_string
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet

from companies.models import Company
from companies.serializers import CompanySerilaizers


# Create your views here.
class CompanyViewSet(ModelViewSet):
    serializer_class = CompanySerilaizers
    queryset = Company.objects.all().order_by("-updated_at")
    pagination_class = PageNumberPagination


@api_view(["POST"])
def send_company_email(request:Request) -> Response:
    plaintext = render_to_string("../templates/welcome_email.txt")
    html_text = render_to_string("../templates/welcome_email.html")

    mail.send_mail(
        subject=request.data.get("subject"),
        message=plaintext,
        from_email="send@mail.com",
        recipient_list=["recieve@mail.com"],
        html_message=html_text,
    )
    return Response({"status":"success","info":"email sent successfully"},status=200)
