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
    # random_sufix = random.randint(0, 10)
    # return generate_username(1)[0] + str(random_sufix)
    return generate_username(1)[0]


# This method generates a random email based on the first and last name
def get_email(f_name, l_name):
    email = None
    suffix = fake.email().split("@", 1)[1]
    chance = random.randint(0, 8)
    if chance == 0:
        email = f_name[0].lower() + "." + l_name[0:].lower()
    elif chance == 1:
        email = f_name.lower() + "." + l_name.lower()
    elif chance == 2:
        email = f_name.lower() + l_name.lower()
    elif chance == 3:
        email = l_name.lower() + "." + f_name.lower()
    elif chance == 4:
        email = l_name.lower() + f_name.lower()
    elif chance == 5:
        email = f_name.lower() + l_name[0].lower()
    elif chance == 6:
        email = l_name.lower()[0] + "." + f_name.lower()
    else:
        email = l_name.lower()[0] + f_name.lower()
    email += str(random.randint(0, 10000))
    email += "@" + suffix
    return email


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
        f_name = get_fname()
        l_name = get_lname()
        users.append(User(get_username(), get_email(f_name, l_name), get_pass(), f_name, l_name, get_is_admin()))
    return users


if __name__ == '__main__':
    print(get_email("Wyatt", "Meehan"))
