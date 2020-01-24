from bs4 import BeautifulSoup

import random
import string

from atd_knack_api._utils import knackpy_wrapper, knack_filter



def lookup_connection(val, config, auth):
    """
    This transform is used for the setting of a connection field in the destination app.

    It queries the destination app for a record matching the input value (first apply any
    "pre-transform" that was supplied). If a matching record is found, the record ID is
    returned inside a list, as is required by the Knack API.
    """
    if config.get("pre_transform"):
        """
        Apply another transform function on the input value. this is useful for say, parsing
        an email address from a field
        """
        transform_func = globals().get(config["pre_transform"])
        val = transform_func(val)
    
    filters = knack_filter(config.get("lookup_field_dest"), val)
    kn = knackpy_wrapper({"obj" : config["object_key_dest"]}, auth, filters)
    
    if (kn.data_raw):
        # we take the first record that matches our filter. assume the `lookup_field_dest` val is unique
        # we transform it to a knack connection list
        return [kn.data_raw[0]["id"]]
    else:
        return None

    

def text_to_connection(val):
    """
    Return a Knack connection list from a str
    """
    if val:
        return [val]
    else:
        return []


def handle_html(html):
    """
    Receive a single Knack html tag and value.

    E.g., email address
    """
    soup = BeautifulSoup(html, "html5lib")
    return soup.get_text()


def random_password(val, length=30):
    """
    Generate a random string with the combination of lowercase and uppercase letters
    numbers, and punctuation.

    The input value here is to be ignored. It is passed from a Knack account record as "*******"
    """
    alphanum = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(alphanum) for i in range(length))