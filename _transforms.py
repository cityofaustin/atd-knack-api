def text_to_connection(val):
    """
    Return a Knack connection list from a str
    """
    if val:
        return [val]
    else:
        return []