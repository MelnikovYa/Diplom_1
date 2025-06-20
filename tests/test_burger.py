import pytest
from unittest.mock import MagicMock
from praktikum.burger import Burger
from praktikum.bun import Bun
from praktikum.ingredient import Ingredient


@pytest.fixture
def bun():
    return Bun("Test Bun", 50.0)


@pytest.fixture
def sauce():
    return Ingredient("SAUCE", "Test Sauce", 20.0)


@pytest.fixture
def filling():
    return Ingredient("FILLING", "Test Filling", 30.0)


@pytest.fixture
def burger():
    return Burger()


def test_set_buns(burger, bun):
    burger.set_buns(bun)
    assert burger.bun is bun


def test_add_ingredient(burger, sauce):
    burger.add_ingredient(sauce)
    assert sauce in burger.ingredients


def test_remove_ingredient(burger, sauce):
    burger.add_ingredient(sauce)
    burger.remove_ingredient(0)
    assert len(burger.ingredients) == 0


def test_move_ingredient(burger, sauce, filling):
    burger.add_ingredient(sauce)
    burger.add_ingredient(filling)
    burger.move_ingredient(0, 1)
    assert burger.ingredients[1] == sauce


@pytest.mark.parametrize("bun_price, ingredient_prices, expected_price", [
    (50, [20, 30], 50 * 2 + 20 + 30),
    (100, [], 100 * 2),
    (75, [25, 25, 25], 75 * 2 + 75),
])
def test_get_price(bun_price, ingredient_prices, expected_price):
    mock_bun = MagicMock()
    mock_bun.get_price.return_value = bun_price
    burger = Burger()
    burger.set_buns(mock_bun)
    for price in ingredient_prices:
        mock_ingredient = MagicMock()
        mock_ingredient.get_price.return_value = price
        burger.add_ingredient(mock_ingredient)
    assert burger.get_price() == expected_price


@pytest.fixture
def sample_burger(bun, sauce, filling):
    burger = Burger()
    burger.set_buns(bun)
    burger.add_ingredient(sauce)
    burger.add_ingredient(filling)
    return burger


def test_receipt_contains_bun_name(sample_burger, bun):
    receipt = sample_burger.get_receipt()
    assert bun.get_name() in receipt


def test_receipt_contains_sauce_name(sample_burger, sauce):
    receipt = sample_burger.get_receipt()
    assert sauce.get_name() in receipt


def test_receipt_contains_filling_name(sample_burger, filling):
    receipt = sample_burger.get_receipt()
    assert filling.get_name() in receipt


def test_receipt_contains_price(sample_burger):
    receipt = sample_burger.get_receipt()
    assert "Price: " in receipt
