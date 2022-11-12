from rest_framework import serializers
from .models import Company


class CompanySerilaizers(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"
        read_only_fields = ["id","created_at","updated_at"]
