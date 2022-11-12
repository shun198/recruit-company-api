from django.db import models

# Create your models here.
class Company(models.Model):
    class CompanyStatus(models.IntegerChoices):
        HIRING = 0
        HIRING_FREEZE = 1
        LAYOFFS = 2

    name = models.CharField(max_length=30, unique=True)
    status = models.IntegerField(
        choices=CompanyStatus.choices, default=CompanyStatus.HIRING
    )
    application_link = models.URLField(blank=True)
    notes = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
