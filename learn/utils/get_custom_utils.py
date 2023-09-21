def custom_get(dictionary, key, default=None):
    try:
        return dictionary[key]
    except KeyError:
        return default
