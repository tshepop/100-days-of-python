from menu import Menu, MenuItem
from coffee_maker import CoffeeMaker
from money_machine import MoneyMachine

drink_resources = CoffeeMaker()
drink_cost = MoneyMachine()
menu = Menu()

my_coffee = True

while my_coffee:
    choice = input(f"What would you like? {menu.get_items()}")

    if choice == "off":
        my_coffee = False
    elif choice == "report":
        drink_resources.report()
        drink_cost.report()
    else:
        drink = menu.find_drink(choice)

        if drink_resources.is_resource_sufficient(drink):
            if drink_cost.make_payment(drink.cost):
                drink_resources.make_coffee(drink)
