from django.test import TestCase
import pytest

# Create your tests here.
def test_right_addition() -> None:
    assert 1 == 1


# mark.skipデコレータを入れてテストをスキップ
@pytest.mark.skip
def test_wrong_addition() -> None:
    assert 1 == 2


# 4>1=Trueのためテストをスキップする
@pytest.mark.skipif(4 > 1, reason="Skipped because 4>1")
def test_wrong_addition_if_skipped() -> None:
    assert 1 == 2


# 0>1=Falseのためテストをスキップしない
# @pytest.mark.skipif(0>1,reason="Skipped because 4>1")
# def test_wrong_addition_if_not_skipped() -> None:
#     assert 1 == 2

# テスト自体は失敗しているのでxfailed
@pytest.mark.xfail
def test_wrong_addition_if_not_skipped() -> None:
    assert 1 == 2


# 異常テスト
# テスト自体は失敗してもいいけどGitHub Actionsを失敗させたくないときxfailを使う
# テスト自体は合っているのでxpassed
@pytest.mark.xfail
def test_dont_care_if_fails_right() -> None:
    assert 1 == 1


# テスト自体は失敗しているのでxfailed
@pytest.mark.xfail
def test_dont_care_if_fails_wrong() -> None:
    assert 1 == 2


# fixtures inside pytest practice files
class Company(object):
    def __init__(self, name: str, stock_symbol: str):
        self.name = name
        self.stock_symbol = stock_symbol

    def __str__(self) -> str:
        return f"{self.name}:{self.stock_symbol}"


@pytest.fixture
def company() -> Company:
    return Company(name="Tesla", stock_symbol="TSLA")


def test_with_fixture(company: Company) -> None:
    print(f"Printing {company} from fixture")


@pytest.mark.parametrize(
    "company_name",
    ["Alibaba", "Tencent", "Huawei"],
    ids=["Alibaba test", "Tencent test", "Huawei test"],
)
def test_parametrized(company_name: str) -> None:
    print(f"\nTest with {company_name}")


def raise_expection() -> None:
    raise ValueError("Test Exception")


def test_raise_expection_should_pass() -> None:
    with pytest.raises(ValueError) as e:
        raise_expection()
    assert "Test Exception" == str(e.value)
