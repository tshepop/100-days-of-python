from data import MENU, resources

# Coffee machine project


resources = {
    "water": 300,
    "milk": 200,
    "coffee": 100,
}

money = 0
profit = 0


def displayReport():
    global money

    print("COFFEE MACHINE MAKER".center(26, "-"))
    print("Available resources:")
    print()

    water = f"{resources.setdefault('water', 0)}ml".rjust(10, " ")
    milk = f"{resources.setdefault('milk', 0)}ml".rjust(10, " ")
    coffee = f"{resources.setdefault('coffee', 0)}g".rjust(10, " ")
    money = f"${money}".rjust(10, " ")

    print("Water ".ljust(15, ".") + water)
    print("Milk ".ljust(15, ".") + milk)
    print("Coffee ".ljust(15, ".") + coffee)
    print("Cost ".ljust(15, ".") + money)


def check_resources(order_resources, drink_ingredients):
    """Check resources if they are enough to make a drink and return True else False"""
    for item in drink_ingredients:
        if drink_ingredients[item] >= order_resources[item]:
            print(f"Sorry, there is not enough {item}!")
            return False
    return True
