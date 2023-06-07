import random
import string

def generate_order_id(length=8):
    characters = string.ascii_uppercase + string.digits
    order_id = ''.join(random.choices(characters, k=length))
    return order_id
