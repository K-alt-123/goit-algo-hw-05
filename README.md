# Substring search

Python 3.12+; standard library only. The two required articles are bundled, so the benchmark needs no network connection.

```powershell
python -m unittest discover -s tests -v
python benchmark.py --help
python benchmark.py
```

Read [the measured report](results/search_report.md) for comparisons per text and overall; [raw timings](results/search.csv) retain every repeat. The overall winner minimizes the equal-weight mean of the four case medians. Timing includes prefix/shift/hash preparation and search, excluding file loading.

All three functions in `searches.py` accept `(text, pattern)` and return the first matching character index, or `-1`. An empty pattern returns `0`. They operate on decoded Unicode characters; they do not normalize case or whitespace.

- `boyer_moore_search` follows the course's right-to-left, shift-table variant (Boyer–Moore–Horspool).
- `kmp_search` constructs a prefix table and reuses matched prefixes.
- `rabin_karp_search` uses base 256, modulus 101, and an exact substring comparison whenever hashes agree. Hash collisions cannot produce an incorrect match.

The original input bytes are retained and explicitly decoded using Windows-1251. Article 1 concerns algorithms in programming-language libraries; article 2 concerns data structures for a social-network recommendation database. Checksums and exact character counts are recorded in the generated report. `data/patterns.json` fixes a present and absent pattern for each article before timing.
