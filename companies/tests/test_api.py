import json
import pytest
from unittest import TestCase

from django.test import Client
from django.urls import reverse

from companies.models import Company


@pytest.mark.django_db
class BaseCompanyAPITestCase(TestCase):
    # 毎回テストの前に実行される
    def setUp(self) -> None:
        self.client = Client()
        self.companies_url = reverse("companies-list")

    # 毎回テストの後に実行される
    def tearDown(self) -> None:
        pass


class TestGetCompanies(BaseCompanyAPITestCase):
    def test_zero_companies_should_return_empty_list(self) -> None:
        response = self.client.get(self.companies_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), [])

    def test_one_company_exists_should_succeed(self) -> None:
        test_company = Company.objects.create(name="Tesla")
        response = self.client.get(self.companies_url)
        response_content = json.loads(response.content)[0]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_content.get("name"), test_company.name)
        self.assertEqual(response_content.get("status"), test_company.status)
        self.assertEqual(
            response_content.get("application_link"), test_company.application_link
        )
        self.assertEqual(response_content.get("notes"), test_company.notes)

        test_company.delete()


class TestPostCompanies(BaseCompanyAPITestCase):
    # 必須項目(name)なしでpostした時
    def test_create_company_without_arguments_should_fail(self) -> None:
        response = self.client.post(path=self.companies_url)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            json.loads(response.content),{"name":["この項目は必須です。"]}
        )

    # すでにある会社をpostした時
    def test_create_existing_companies_should_fail(self) -> None:
        test_company = Company.objects.create(name="Apple")
        response = self.client.post(path=self.companies_url,data={"name":test_company.name})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            json.loads(response.content),{"name":["この name を持った company が既に存在します。"]}
        )

    # 必須項目(name)のみ入力した状態でpostした時
    def test_create_company_with_only_name_all_fields_should_be_default(self) -> None:
        response = self.client.post(path=self.companies_url,data={"name":"test company name"})
        response_content = json.loads(response.content)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_content.get("status"), 0)
        self.assertEqual(response_content.get("application_link"), "")
        self.assertEqual(response_content.get("notes"), "")
