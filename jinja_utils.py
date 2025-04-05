def random_string(length: int = 16) -> str:
    import random
    import string
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for i in range(length))

jinja_utils = {
    "random_string": random_string,
}
