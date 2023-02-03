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

    print()
    print("COFFEE MACHINE MAKER REPORT".center(26, "-"))
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
    print()


def check_resources(order_resources, drink_ingredients):
    """Check resources if they are enough to make a drink and return True else False"""
    for item in drink_ingredients:
        if drink_ingredients[item] >= order_resources[item]:
            print(f"Sorry, there is not enough {item}!")
            return False
    return True


def make_coffee(start_order_resources, drink_ingredients):
    """Deduct/minus drink ingredients from main resources and return"""
    for item in drink_ingredients:
        start_order_resources[item] -= drink_ingredients[item]
    return start_order_resources


drinks_list = []


def print_profit():
    print("-" * 25)
    print("daily profit report".upper().center(25, " "))
    print("-" * 25)
    counter = 0
    for i in range(len(drinks_list)):
        counter += 1
        print(f"Drink sold: {drinks_list[i]}")

    print(f"No. of drinks sold: {counter}")
    print("-" * 25)
    print(f"Todays profit: ${profit}")


QUARTER = 0.25
DIME = 0.10
NICKLE = 0.05
PENNY = 0.01

turn_off = True

while turn_off:
    coffee_type = input("What would you like? (espresso/latte/cappuccino): ")

    if coffee_type == "off":
        turn_off = False
    elif coffee_type == "report":
        displayReport()
    elif coffee_type == "latte":
        drink = MENU[coffee_type]

        if check_resources(resources, drink["ingredients"]):

            print("Please enter coins:")
            c_quarter = float(input("How many quarters? "))
            c_dimes = float(input("How many dimes? "))
            c_nickles = float(input("How many nickles? "))
            c_pennies = float(input("How many pennies? "))
            coin = (QUARTER * c_quarter) + (DIME * c_dimes) + (NICKLE * c_nickles) + \
                (PENNY * c_pennies)

            coin = round(coin, 2)
            # assign drink cost to money variable, which is a global variable
            money = drink["cost"]
            # test to see if enough coins, then pay for drink
            if coin < money:
                print(f"Sorry that not enough money. ${coin} refunded.")
            else:
                print("-" * 25)
                resources = make_coffee(resources, drink["ingredients"])
                profit += money
                drinks_list.append(coffee_type)
                print(f"Here is your {coffee_type}. Enjoy!")
                print(f"Here is ${coin} dollars in change.")

    elif coffee_type == "espresso":
        drink = MENU[coffee_type]

        if check_resources(resources, drink["ingredients"]):

            print("Please enter coins:")
            c_quarter = float(input("How many quarters? "))
            c_dimes = float(input("How many dimes? "))
            c_nickles = float(input("How many nickles? "))
            c_pennies = float(input("How many pennies? "))
            coin = (QUARTER * c_quarter) + (DIME * c_dimes) + (NICKLE * c_nickles) + \
                (PENNY * c_pennies)

            coin = round(coin, 2)
            # assign drink cost to money variable, which is a global variable
            money = drink["cost"]
            # test to see if enough coins, then pay for drink
            if coin < money:
                print(f"Sorry that's not enough money. ${coin} refunded.")
            else:
                print("-" * 25)
                resources = make_coffee(resources, drink["ingredients"])
                profit += money
                drinks_list.append(coffee_type)
                print(f"Here is your {coffee_type}. Enjoy!")
                print(f"Here is ${coin} dollars in change.")

    elif coffee_type == "cappuccino":
        drink = MENU[coffee_type]

        if check_resources(resources, drink["ingredients"]):

            print("Please enter coins:")
            c_quarter = float(input("How many quarters? "))
            c_dimes = float(input("How many dimes? "))
            c_nickles = float(input("How many nickles? "))
            c_pennies = float(input("How many pennies? "))
            coin = (QUARTER * c_quarter) + (DIME * c_dimes) + \
                (NICKLE * c_nickles) + (PENNY * c_pennies)

            coin = round(coin, 2)
            # assign drink cost to money variable, which is a global variable
            money = drink["cost"]
            # test to see if enough coins, then pay for drink
            if coin < money:
                print(
                    f"Sorry that's not enough money. ${coin} refunded.")
            else:
                print("-" * 25)
                resources = make_coffee(resources, drink["ingredients"])
                profit += money
                drinks_list.append(coffee_type)
                print(f"Here is your {coffee_type}. Enjoy!")
                print(f"Here is ${coin} dollars in change.")

print_profit()
