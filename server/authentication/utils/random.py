import string
import random

def random_passwd():
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    password = [
        random.choice(string.ascii_lowercase),  
        random.choice(string.ascii_uppercase),  
        random.choice(string.digits),          
        random.choice("!@#$%^&*")             
    ]

    password += random.choices(chars, k=15)
    random.shuffle(password)
    password = ''.join(password)

    return password