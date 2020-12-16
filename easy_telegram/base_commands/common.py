from typing import List


def get_msg_content(text: str) -> List[str]:
    """
    returns the message without the first word, which would be the command
    :param text: the raw message.text
    :return: the message without the first word, None if there was nothing
    """
    words: List[str] = text.split(" ")
    if len(words) < 2:
        return []
    words.pop(0)
    return words
