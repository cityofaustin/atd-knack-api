from bs4 import BeautifulSoup

import random
import string

from atd_knack_api._utils import knackpy_wrapper, knack_filter


"""
The lookup cache obviate's the need to make repeated lookup calls to the api. For example,
multiple transactions may be connected to the same work order record ID. Instead of fetching
this value for each transaction record, the value is stored in this global cache. The keys
in the cache follow the format `{lookup_field_dest}__&__{val}`. E.g. a work order record
would be stored as `WRK20-019384__&__am49c04mc4834al2
"""
LOOKUP_CACHE = {}
CACHE_DELIMTTER = "__&__"

def lookup(val, config, auth):

    if not val:
        return None
    """
    This transform is used for fetching the knack record ID from the the destination
    application, and returning the record ID as a str or list, as defined in the
    `connection` key in the transform config. A list is returned for the purposes
    of setting connection fields, a str is returned for the purpose of setting the
    record ID of a record to be updated.

    It queries the destination app for a record matching the input value (first applying
    any "pre-transform" that was supplied). If a matching record is found, it is returned,
    else None is returned
    """
    if config.get("pre_transform"):
        """
        Apply another transform function on the input value. this is useful for say, parsing
        an email address from a field
        """
        transform_func = globals().get(config["pre_transform"])
        val = transform_func(val)
    
    lookup_field_dest = config.get("lookup_field_dest")
    cache_key = f"{lookup_field_dest}{CACHE_DELIMTTER}{val}"

    if cache_key in LOOKUP_CACHE:
        return LOOKUP_CACHE[cache_key]

    # if value is not cached, fetch it from Knack
    filters = knack_filter(lookup_field_dest, val)

    kn = knackpy_wrapper({"obj" : config["object_key_dest"]}, auth, filters)
    
    if (kn.data_raw):
        # we take the first record that matches our filter. assume the `lookup_field_dest` val is unique
        # we transform it to a knack connection list
        if config.get("connection"):
            val_transformed = [kn.data_raw[0]["id"]]
        else:
            val_transformed = kn.data_raw[0]["id"]

        LOOKUP_CACHE[f"{lookup_field_dest}{CACHE_DELIMTTER}{val}"] = val_transformed
        return val_transformed
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
    if not html:
        return None

    soup = BeautifulSoup(html)
    return soup.get_text()


def random_password(val, length=30):
    """
    Generate a random string with the combination of lowercase and uppercase letters
    numbers, and punctuation.

    The input value here is to be ignored. It is passed from a Knack account record as "*******"
    """
    alphanum = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(alphanum) for i in range(length))