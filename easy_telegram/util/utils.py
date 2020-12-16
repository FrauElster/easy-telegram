import os


def get_env(env_var: str, type_: type = str, default=None):
    val = os.getenv(env_var, default)
    if val is None:
        if type_ is not None:
            raise ValueError(f'"{env_var}" not set')
        return val
    try:
        return type_(val)
    except ValueError as e:
        raise ValueError(f'"{env_var}" has to be of type "{type_}". Failed to convert: {e}')


def levenshtein(s1: str, s2: str) -> int:
    """
    Calculates the levenshtein distance of the given strings
    :param s1:
    :param s2:
    :return:
    """
    if len(s1) < len(s2):
        return levenshtein(s2, s1)

    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]
