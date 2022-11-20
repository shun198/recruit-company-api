import requests
import json

testing_env_companies_url = "http://127.0.0.1:8000/api/companies/"


# def test_get_companies_django_agnostic() -> None:
#     response = requests.get(url=testing_env_companies_url)
#     assert response.status_code == 200
#     assert json.loads(response.content) == []


# def test_create_company_with_layoffs_django_agnostic(client) -> None:
#     response = requests.post(
#         url=testing_env_companies_url, json={"name": "test company name", "status": 2}
#     )
#     assert response.status_code == 201
#     response_content = json.loads(response.content)
#     assert response_content.get("status") == 2
