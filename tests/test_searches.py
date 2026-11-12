import itertools
import random
import unittest

from searches import boyer_moore_search, kmp_search, rabin_karp_search


class SearchTests(unittest.TestCase):
    def test_boundary_cases(self):
        cases = [('', ''), ('', 'x'), ('abc', ''), ('abc', 'abc'), ('abc', 'd'),
                 ('abc', 'abcd'), ('aaaaab', 'aaab'), ('ababababac', 'ababac'),
                 ('Привіт, світе', 'світе'), ('🙂x🙂y', '🙂y'), ('abc', 'c')]
        for text, pattern in cases:
            for function in (boyer_moore_search, kmp_search, rabin_karp_search):
                with self.subTest(function=function.__name__, text=text, pattern=pattern):
                    self.assertEqual(function(text, pattern), text.find(pattern))

    def test_generated_cases_against_builtin(self):
        rng = random.Random(97)
        for _ in range(700):
            text = ''.join(rng.choices('abв🙂', k=rng.randrange(80)))
            pattern = ''.join(rng.choices('abв🙂', k=rng.randrange(12)))
            for function in (boyer_moore_search, kmp_search, rabin_karp_search):
                self.assertEqual(function(text, pattern), text.find(pattern))

    def test_rabin_karp_verifies_hash_collisions(self):
        # Base 256 modulo 101: hash('ab') == hash('b,') == 84.
        self.assertEqual(rabin_karp_search('ab', 'b,'), -1)
        self.assertEqual(rabin_karp_search('ab---b,', 'b,'), 5)


if __name__ == '__main__':
    unittest.main()
