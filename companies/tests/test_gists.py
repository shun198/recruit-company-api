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
@pytest.mark.skipif(4>1,reason="Skipped because 4>1")
def test_wrong_addition_if_skipped() -> None:
    assert 1 == 2

# 0>1=Falseのためテストをスキップしない
# @pytest.mark.skipif(0>1,reason="Skipped because 4>1")
# def test_wrong_addition_if_not_skipped() -> None:
#     assert 1 == 2

# 異常テスト
# テスト自体は失敗してもいいけどGitHub Actionsを失敗させたくない
@pytest.mark.xfail
def test_dont_care_if_fails_right() -> None:
    assert 1 == 1

@pytest.mark.xfail
def test_dont_care_if_fails_wrong() -> None:
    assert 1 == 2

# fixture
class Company(object):
    def __init__(self, name:str, stock_symbol:str):
        self.name = name
        self.stock_symbol = stock_symbol

    def __str__(self) -> str:
        return f"{self.name}:{self.stock_symbol}"

@pytest.fixture
def company() -> Company:
    return Company(name="Tesla",stock_symbol="TSLA")

