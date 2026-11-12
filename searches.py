"""First-match substring searches; indexes refer to Unicode characters."""


def boyer_moore_search(text: str, pattern: str) -> int:
    """Course variant: right-to-left comparison with Horspool bad-character shifts."""
    size = len(pattern)
    if size == 0:
        return 0
    shifts = {char: size - index - 1 for index, char in enumerate(pattern[:-1])}
    start = 0
    while start <= len(text) - size:
        index = size - 1
        while index >= 0 and text[start + index] == pattern[index]:
            index -= 1
        if index < 0:
            return start
        start += shifts.get(text[start + size - 1], size)
    return -1


def prefix_table(pattern: str) -> list[int]:
    prefix = [0] * len(pattern)
    length = 0
    for index in range(1, len(pattern)):
        while length and pattern[index] != pattern[length]:
            length = prefix[length - 1]
        if pattern[index] == pattern[length]:
            length += 1
        prefix[index] = length
    return prefix


def kmp_search(text: str, pattern: str) -> int:
    if not pattern:
        return 0
    prefix, matched = prefix_table(pattern), 0
    for index, char in enumerate(text):
        while matched and char != pattern[matched]:
            matched = prefix[matched - 1]
        if char == pattern[matched]:
            matched += 1
        if matched == len(pattern):
            return index - len(pattern) + 1
    return -1


def rabin_karp_search(text: str, pattern: str) -> int:
    size = len(pattern)
    if size == 0:
        return 0
    if size > len(text):
        return -1
    base, modulus = 256, 101
    leading_weight = pow(base, size - 1, modulus)
    pattern_hash = window_hash = 0
    for index in range(size):
        pattern_hash = (base * pattern_hash + ord(pattern[index])) % modulus
        window_hash = (base * window_hash + ord(text[index])) % modulus
    for start in range(len(text) - size + 1):
        if window_hash == pattern_hash and text[start:start + size] == pattern:
            return start
        if start < len(text) - size:
            window_hash = (base * (window_hash - ord(text[start]) * leading_weight)
                           + ord(text[start + size])) % modulus
    return -1
