from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from companies.serializers import CompanySerilaizers
from companies.models import Company

# Create your views here.
class CompanyViewSet(ModelViewSet):
    serializer_class = CompanySerilaizers
    queryset = Company.objects.all().order_by("-updated_at")
    pagination_class = PageNumberPagination
