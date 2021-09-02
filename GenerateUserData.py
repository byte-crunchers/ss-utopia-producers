import random

from faker import Faker
from random_username.generate import generate_username

fake = Faker()


class User:
    def __init__(self, user, email, password, f_name, l_name, is_admin):
        self.user = user
        self.email = email
        self.password = password
        self.f_name = f_name
        self.l_name = l_name
        self.is_admin = is_admin


def get_username():
    random_sufix = random.randint(0, 10000)
    return generate_username(1)[0] + str(random_sufix)


def get_email():
    return fake.email()


def get_pass():
    password_length = random.randint(8, 15)
    possible_characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890"
    random_character_list = [random.choice(possible_characters) for i in range(password_length)]
    return "".join(random_character_list)


def get_fname():
    return fake.first_name()


def get_lname():
    return fake.last_name()


def get_is_admin():
    chance = random.randint(0, 10)
    if chance >= 2:
        return False
    else:
        return True


def get_user_data(num_of_users):
    users = []
    for x in range(num_of_users):
        users.append(User(get_username(), get_email(), get_pass(), get_fname(), get_lname(), get_is_admin()))
    return users
