import random
import string


def generate_password():
    length = 6
    chars = string.punctuation + string.digits

    rnd = random.SystemRandom()
    password = ''.join(rnd.choice(chars) for _ in range(length))
    return password
