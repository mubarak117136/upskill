import re
import os

def check_bd_phone_number(phone_number):
    expression = r"^(?:\+88|01)?(?:\d{11}|\d{13})$"
    check = re.match(expression, str(phone_number), flags=0)
    return True if check else False


def check_email(email):
    return re.match('^[_a-zA-Z0-9-]+(\.[_a-zA-Z0-9-]+)*@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*(\.[a-zA-Z]{2,4})$', email)
    