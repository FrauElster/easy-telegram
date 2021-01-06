import logging
import os


def get_env(env_var: str, type_: type = str, default=None):
    val = os.getenv(env_var, default)
    if val is None:
        if type_ is not None:
            raise ValueError(f'"{env_var}" not set')
        return val
    try:
        return type_(val)
    except ValueError as err:
        raise ValueError(f'"{env_var}" has to be of type "{type_}". Failed to convert: {err}') from err


def levenshtein(word_one: str, word_two: str) -> int:
    """
    Calculates the levenshtein distance of the given strings
    :param word_one:
    :param word_two:
    :return:
    """
    if len(word_one) < len(word_two):
        word_one, word_two = word_two, word_one

    if len(word_two) == 0:
        return len(word_one)

    previous_row = list(range(len(word_two) + 1))
    for i, c1 in enumerate(word_one):
        current_row = [i + 1]
        for j, c2 in enumerate(word_two):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]
