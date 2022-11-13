import json
import pytest
import logging
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
    # 会社がない場合は空で帰ってくる(Companyのobjectを作成していないため)
    def test_zero_companies_should_return_empty_list(self) -> None:
        response = self.client.get(self.companies_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), [])

    def test_one_company_exists_should_succeed(self) -> None:
        # Companyのobjectを作成しているだけで値はデフォルトで入ってくるステータスと定義した名前しか入ってない
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
        self.assertEqual(json.loads(response.content), {"name": ["この項目は必須です。"]})

    # すでにある会社をpostした時
    def test_create_existing_companies_should_fail(self) -> None:
        test_company = Company.objects.create(name="Apple")
        response = self.client.post(
            path=self.companies_url, data={"name": test_company.name}
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            json.loads(response.content), {"name": ["この name を持った company が既に存在します。"]}
        )

    # 必須項目(name)のみ入力した状態でpostした時
    def test_create_company_with_only_name_all_fields_should_be_default(self) -> None:
        response = self.client.post(
            path=self.companies_url, data={"name": "test company name"}
        )
        response_content = json.loads(response.content)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_content.get("status"), 0)
        self.assertEqual(response_content.get("application_link"), "")
        self.assertEqual(response_content.get("notes"), "")

    def test_create_company_with_layoffs_status_should_succeed(self) -> None:
        response = self.client.post(
            path=self.companies_url, data={"name": "test company name", "status": 2}
        )
        response_content = json.loads(response.content)
        # layoff
        self.assertEqual(response_content.get("status"), 2)

    def test_create_company_with_wrong_status_should_fail(self) -> None:
        response = self.client.post(
            path=self.companies_url, data={"name": "test company name", "status": 3}
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("Bad Request", str(response.status_text))


# Exception
def raise_covid19_exception() -> None:
    raise ValueError("CoronaVirus Exception")


def test_raise_covid19_exception_should_pass() -> None:
    with pytest.raises(ValueError) as e:
        raise_covid19_exception()
    assert "CoronaVirus Exception" == str(e.value)


# logger
logger = logging.getLogger("CORONA_LOGS")


def function_that_logs_something() -> None:
    try:
        raise ValueError("CoronaVirus Exception")
    except ValueError as e:
        logger.warning(f"I am logging {str(e)}")


def test_logged_warning_level(caplog) -> None:
    function_that_logs_something()
    assert "I am logging CoronaVirus Exception" in caplog.text


def test_logged_info_level(caplog) -> None:
    with caplog.at_level(logging.INFO):
        logger.info("I am logging info level")
        assert "I am logging info level" in caplog.text
