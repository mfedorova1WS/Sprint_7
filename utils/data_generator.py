import requests
import random
import string
import time

def generate_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def register_new_courier_and_return_login_password():
    login = generate_random_string(10) + str(int(time.time()))
    password = generate_random_string(10) + str(int(time.time()))
    first_name = generate_random_string(10) + str(int(time.time()))
    return [login, password, first_name]