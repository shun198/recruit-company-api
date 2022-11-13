import json
import pytest
import logging

from django.test import Client
from django.urls import reverse

from companies.models import Company

companies_url = reverse("companies-list")
# pytestのmarkerをimportレベルで書く
# 全てのテストは独立していてお互い干渉しあわない
pytestmark = pytest.mark.django_db


def test_zero_companies_should_return_empty_list(client) -> None:
    response = client.get(companies_url)
    assert response.status_code == 200
    assert json.loads(response.content) == []


def test_one_company_exists_should_succeed(client) -> None:
    # Companyのobjectを作成しているだけで値はデフォルトで入ってくるステータスと定義した名前しか入ってない
    test_company = Company.objects.create(name="Tesla")
    response = client.get(companies_url)
    response_content = json.loads(response.content)[0]
    assert response.status_code == 200
    assert response_content.get("name") == test_company.name
    assert response_content.get("status") == test_company.status
    assert response_content.get("application_link") == test_company.application_link
    assert response_content.get("notes") == test_company.notes


# 必須項目(name)なしでpostした時
def test_create_company_without_arguments_should_fail(client) -> None:
    response = client.post(path=companies_url)
    assert response.status_code == 400
    assert json.loads(response.content) == {"name": ["この項目は必須です。"]}


# すでにある会社をpostした時
def test_create_existing_companies_should_fail(client) -> None:
    test_company = Company.objects.create(name="Apple")
    response = client.post(path=companies_url, data={"name": test_company.name})
    assert response.status_code == 400
    assert json.loads(response.content) == {"name": ["この name を持った company が既に存在します。"]}


# 必須項目(name)のみ入力した状態でpostした時
def test_create_company_with_only_name_all_fields_should_be_default(client) -> None:
    response = client.post(path=companies_url, data={"name": "test company name"})
    response_content = json.loads(response.content)
    assert response.status_code == 201
    assert response_content.get("status") == 0
    assert response_content.get("application_link") == ""
    assert response_content.get("notes") == ""


def test_create_company_with_layoffs_status_should_succeed(client) -> None:
    response = client.post(
        path=companies_url, data={"name": "test company name", "status": 2}
    )
    response_content = json.loads(response.content)
    # layoff
    assert response_content.get("status") == 2


def test_create_company_with_wrong_status_should_fail(client) -> None:
    response = client.post(
        path=companies_url, data={"name": "test company name", "status": 3}
    )
    assert response.status_code == 400
    assert "Bad Request" in str(response.status_text)


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
