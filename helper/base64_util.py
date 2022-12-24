import base64


def base64_encode(string):
    return base64.b64encode(string.encode()).decode()


def base64_decode(string):
    return base64.b64decode(string).decode()
