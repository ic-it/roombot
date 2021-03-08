def valid_check(string: str):
    valid_chars = "abcdefghijklmnopqrstuvwxyz1234567890_-"
    for char in string:
        if char not in valid_chars:
            return False
    return True
