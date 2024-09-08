import re


def contains_latin(text):
    latin_pattern = re.compile('[a-zA-Z]')
    return bool(latin_pattern.search(text))