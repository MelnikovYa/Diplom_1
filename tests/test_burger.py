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

@pytest.fixture
def sample_burger(bun, sauce, filling):
    burger = Burger()
    burger.set_buns(bun)
    burger.add_ingredient(sauce)
    burger.add_ingredient(filling)
    return burger

class TestBurger:

    def test_set_buns(self, burger, bun):
        burger.set_buns(bun)
        assert burger.bun is bun

    def test_add_ingredient(self, burger, sauce):
        burger.add_ingredient(sauce)
        assert sauce in burger.ingredients

    def test_remove_ingredient(self, burger, sauce):
        burger.add_ingredient(sauce)
        burger.remove_ingredient(0)
        assert len(burger.ingredients) == 0

    def test_move_ingredient(self, burger, sauce, filling):
        burger.add_ingredient(sauce)
        burger.add_ingredient(filling)
        burger.move_ingredient(0, 1)
        assert burger.ingredients[1] == sauce

    @pytest.mark.parametrize("bun_price, ingredient_prices, expected_price", [
        (50, [20, 30], 50 * 2 + 20 + 30),
        (100, [], 100 * 2),
        (75, [25, 25, 25], 75 * 2 + 75),
    ])
    def test_get_price(self, bun_price, ingredient_prices, expected_price):
        mock_bun = MagicMock()
        mock_bun.get_price.return_value = bun_price
        burger = Burger()
        burger.set_buns(mock_bun)
        for price in ingredient_prices:
            mock_ingredient = MagicMock()
            mock_ingredient.get_price.return_value = price
            burger.add_ingredient(mock_ingredient)
        assert burger.get_price() == expected_price

    def test_get_receipt_returns_correct_format(self, sample_burger, bun, sauce, filling):
        expected_receipt = (
            f"(==== {bun.get_name()} ====)\n"
            f"= {sauce.get_type().lower()} {sauce.get_name()} =\n"
            f"= {filling.get_type().lower()} {filling.get_name()} =\n"
            f"(==== {bun.get_name()} ====)\n\n"
            f"Price: {sample_burger.get_price()}"
        )

        actual_receipt = sample_burger.get_receipt()
        assert actual_receipt == expected_receipt