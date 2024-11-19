import time
import os
from time import sleep

os.system('cls' if os.name == 'nt' else 'clear')  # Очищення консолі після кожного запуску для зручності

login_success = False
username = ""


def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')


def load_users():
    users = {"admin": {"pin": "admin1234", "balance": 0}}
    try:
        with open("users.txt", "r") as file:
            for line in file:
                username, pin, balance = line.strip().split(",")
                users[username] = {"pin": pin, "balance": int(balance)}
    except FileNotFoundError:
        pass
    return users


def load_blocked_users():
    blocked_users = set()
    try:
        with open("blocked_users.txt", "r") as file:
            for line in file:
                blocked_users.add(line.strip())
    except FileNotFoundError:
        pass
    return blocked_users


def save_users(users):
    with open("users.txt", "w") as file:
        for username, info in users.items():
            file.write(f"{username},{info['pin']},{info['balance']}\n")


def save_blocked_users(blocked_users):
    with open("blocked_users.txt", "w") as file:
        for user in blocked_users:
            file.write(f"{user}\n")


def read_session():
    try:
        with open("session.txt", "r") as file:
            last_session = file.read()
        return last_session
    except FileNotFoundError:
        return None


def write_session(username):
    with open("session.txt", "w") as file:
        file.write(username)


def register(users):
    time.sleep(1)
    print("-------------------------------------------")
    username = input("Введіть ім'я користувача: ")
    time.sleep(0.5)
    while username in users:
        print("Користувач вже існує!")
        time.sleep(0.5)
        username = input("Введіть ім'я користувача: ")

    pin = input("Введіть пін-код: ")
    time.sleep(0.5)
    confirm_pin = input("Підтвердьте пін-код: ")
    time.sleep(0.5)

    while confirm_pin != pin:
        time.sleep(1)
        print("Пін-коди не збігаються! Спробуйте ще раз!")
        time.sleep(1)
        confirm_pin = input("Підтвердьте пін-код: ")

    users[username] = {"pin": pin, "balance": 0}

    with open("users.txt", "a") as file:
        file.write(f"{username},{pin},0\n")

    time.sleep(1)
    print("-------------------------------------------")

    print("Данні додано успішно!\n")


def login(users, blocked_users):
    global login_success
    while True:
        time.sleep(1)
        print("-------------------------------------------")
        username = input("Введіть своє ім'я користувача:\n")
        if username in blocked_users:
            time.sleep(1)
            print("-------------------------------------------")
            return "Ваш рахунок заблокований!"  # Повертається повідомлення про блокування

        if username in users:
            time.sleep(1)
            print("-------------------------------------------")
            break
        else:
            time.sleep(1)
            print("Ім'я користувача не знайдено!")

    attempts = 0
    while attempts < 3:
        pin = input("Введіть свій пін-код:\n")
        if users[username]["pin"] == pin:
            time.sleep(1)
            print("-------------------------------------------")
            print("\n~~~~~~~~~~~~~~~~~~~~~~~~~\n")
            print(f"Вітаємо, {username}!")
            print("\n~~~~~~~~~~~~~~~~~~~~~~~~~\n")

            choice = input("Чи бажаєте зберегти данні для майбутнього входу?").lower()
            if choice == "так":
                write_session(username)

            login_success = True
            return username  # Повертається ім'я користувача після успішного входу

        else:
            time.sleep(1)
            attempts += 1
            print("Неправильно введений пін-код!")
            print("-------------------------------------------")

    blocked_users.add(username)  # Блокуємо користувача після 3 неправильних спроб
    save_blocked_users(blocked_users)  # Зберігаємо заблокованих
    return "Спроби вичерпано! Рахунок заблоковано!"  # Повертається повідомлення про блокування


def check_balance(users, username):
    time.sleep(1)
    print("~~~~~~~~~~~~~~~~~~~~~~~~~")
    print(f"Ваш баланс становить {users[username]['balance']}ГРН\n")


def deposit(users, username):
    while True:
        amount = input(
            "Введіть суму на яку ви хочете поповнити свій баланс (від 1 до 100,000ГРН) (Введіть С щоб скасувати)\n")
        if amount == "С":
            break

        try:
            amount = int(amount)
            if 0 < amount <= 100000:
                users[username]['balance'] += amount
                time.sleep(1)
                print(f"Ваш новий баланс становить {users[username]['balance']}ГРН\n")
                break
        except ValueError:
            print("Введена некоректна сума, спробуйте ще раз!")


def withdraw(users, username):
    while True:
        amount = input(
            "Введіть суму яку ви хочете зняти з свого рахунку (від 1 до 100,000ГРН) (Введіть С щоб скасувати)\n")
        if amount == "С":
            break

        try:
            amount = int(amount)
            if 0 < amount <= 100000 and users[username]['balance'] >= amount:
                users[username]['balance'] -= amount
                time.sleep(1)
                print(f"Ваш новий баланс становить {users[username]['balance']}ГРН\n")
                break
            elif 0 > amount or 100000 < amount:
                print("Введена недопустима сумма!")
            elif users[username]['balance'] < amount:
                print("На рахунку не вистачає грошей!")
            elif amount is not int:
                print("Введене не число!")
        except ValueError:
            print("Введене некоректне значення!")


def user_interface(users, username):
    time.sleep(1)
    while True:
        choice = input("Що ви бажаєте зробити?\nДепозит: 1\nЗняти гроші: 2\nПеревірити баланс: 3\nВийти: 0\n")

        if choice == "1":
            deposit(users, username)
        elif choice == "2":
            withdraw(users, username)
        elif choice == "3":
            check_balance(users, username)
        elif choice == "0":
            return False
        else:
            print("Не коректний вибір!")


def admin_panel(users, blocked_users):
    time.sleep(1)
    print("~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("Ви можете переглядати баланси користувачів або блокувати/розблоковувати їх.")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~")
    time.sleep(1)

    while True:
        print("-------------------------------------------")
        choice = input("\n\nБаланси або блокування/розблокування (1, 2)\n")
        print("-------------------------------------------")

        if choice == "1":
            search_choice = input("Знайти користувача по імені? (1 - Так, 2 - Показати всіх)\n")

            if search_choice == "1":
                username = input("Введіть ім'я користувача: ")
                if username in users:
                    print(f"{username}: {users[username]['balance']} ГРН\n")
                else:
                    print("Користувача не знайдено!\n")

            elif search_choice == "2":
                for username, info in users.items():
                    print(f"{username}: {info['balance']} ГРН")

            input("\nНатисніть Enter, щоб повернутися.\n")

        elif choice == "2":
            print(f"Заблоковані користувачі:\n")
            for username in blocked_users:
                print(username)
        else:
            print("Не коректний вибір!")

            username = input("Введіть ім'я користувача: ")

            if username in users:
                if username in blocked_users:
                    blocked_users.remove(username)
                    print("Користувача розблоковано!\n")
                else:
                    blocked_users.add(username)
                    print("Користувача заблоковано!\n")
            else:
                print("Користувача не знайдено!\n")


clear_console()
users = load_users()
blocked_users = load_blocked_users()

while True:
    last_user = read_session()

    if login_success != True:
        if last_user != "":
            while True:
                print("-------------------------------------------")
                choice = input(f"Знайдений вхід з попередньої Сесії! Користувач {last_user}\nЧи бажаєте ви її продовжити? (Так/Ні): ").lower()
                print("-------------------------------------------")
                if choice == "так":
                    time.sleep(1)
                    print("Вхід...")
                    username = last_user
                    time.sleep(1)
                    login_success = True
                    break
                elif choice == "ні":
                    last_user = ""
                    write_session("")
                    time.sleep(1)
                    break
                else:
                    print("Некоректний вибір!")

    if username == "admin":
        admin_panel(users, blocked_users)
    else:
        if login_success:
            if not user_interface(users, username):  # Якщо повернено False, завершуємо сесію користувача
                print("Вихід з акаунту.\n")
                login_success = False
                username = ""  # Скидаємо username для виходу
            else:
                print(f"Вітаємо, {username}! Ваш баланс {users[username]['balance']} ГРН.\n")
                input("Натисніть Enter, щоб продовжити...\n")
        else:
            choice = input("Вітаємо в банкоматі!\nВвійти (1)\nРеєстрація(2)\nПокинути банкомат(3)\n")

            if choice == "1":
                username = login(users, blocked_users)
                if username == "Ваш рахунок заблокований!":
                    print(username)
                    time.sleep(1)

            elif choice == "2":
                time.sleep(1)
                register(users)
                save_users(users)

            elif choice == "3":
                time.sleep(1)
                break

            else:
                time.sleep(1)
                print("Не коректний вибір!")
