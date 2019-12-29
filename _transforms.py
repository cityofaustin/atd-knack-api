import random
import string

def text_to_connection(val):
    """
    Return a Knack connection list from a str
    """
    if val:
        return [val]
    else:
        return []

def handle_email(d):
    """
    Receive a raw Knack email dict and return the email str
    """
    if d.get("email"):
        return d.get("email")
    else:
        # this should never happen. email address is required for user accounts
        return ""


def random_password(val, length=30):
    """
    Generate a random string with the combination of lowercase and uppercase letters
    numbers, and punctuation.

    The input value here is to be ignored. It is passed from a Knack account record as "*******"
    """
    alphanum = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(alphanum) for i in range(length))