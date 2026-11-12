# Substring-search measurements

Python 3.14.8; Windows-11-10.0.26300-SP0; 2026-11-11T08:43:55.854185+00:00.

7 timeit repetitions of 30 calls each. Medians below include pattern preprocessing and actual search, but exclude file I/O. Each case uses the same text and pattern for every method. Inputs and fixed patterns are bundled in data/.

article1: 12,785 bytes; 12,785 characters; Windows-1251; SHA-256 `757a2a84ebf2b04d2eec7841f95827acc3689d652c59f87c5541fc685795de1f`.
article2: 18,467 bytes; 18,467 characters; Windows-1251; SHA-256 `9569bdbc871c9f8778fe0585dabc4f4e22b87beab23adc5ddd13341d8865a4a5`.

| Text | Pattern | Boyer–Moore–Horspool (ms) | KMP (ms) | Rabin–Karp (ms) | Fastest |
|---|---|---:|---:|---:|---|
| article1 | present | 0.0893 | 0.5734 | 1.2643 | Boyer-Moore-Horspool |
| article1 | absent | 0.0667 | 0.8813 | 2.2790 | Boyer-Moore-Horspool |
| article2 | present | 0.1177 | 0.7285 | 1.8603 | Boyer-Moore-Horspool |
| article2 | absent | 0.1008 | 1.3173 | 3.5812 | Boyer-Moore-Horspool |

## Conclusions

article1: Boyer-Moore-Horspool has the lowest mean of the present/absent case medians (0.0780 ms).
article2: Boyer-Moore-Horspool has the lowest mean of the present/absent case medians (0.1093 ms).
Overall: Boyer-Moore-Horspool has the lowest equally weighted mean of the four case medians (0.0936 ms).

Boyer–Moore–Horspool can skip sections of text; KMP avoids rechecking matched prefixes and has O(n + m) worst-case time. Rabin–Karp updates a rolling hash but must verify matching hashes to avoid false matches. Its small modulus deliberately makes collision handling visible and can increase verification work.
These findings concern the bundled Ukrainian articles and four fixed patterns. Pattern length, match position, repetition, encoding choices, and implementation overhead can change the result. They do not prove a universal ranking.

The course calls its shift-table method Boyer–Moore. The implementation here is its bad-character-only Horspool variant, not the full good-suffix version.
