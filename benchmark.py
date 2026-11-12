"""Time the three search methods on the two assigned articles."""
import argparse
import csv
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import statistics
import timeit

from searches import boyer_moore_search, kmp_search, rabin_karp_search


def benchmark(output: Path, repeats=7, number=30):
    base = Path(__file__).resolve().parent
    patterns = json.loads((base / 'data/patterns.json').read_text(encoding='utf-8'))
    algorithms = {'Boyer-Moore-Horspool': boyer_moore_search, 'KMP': kmp_search, 'Rabin-Karp': rabin_karp_search}
    rows, medians, identities = [], {}, []
    for article in ('article1', 'article2'):
        raw = (base / f'data/{article}.txt').read_bytes()
        text = raw.decode('cp1251')
        identities.append(f'{article}: {len(raw):,} bytes; {len(text):,} characters; Windows-1251; SHA-256 `{hashlib.sha256(raw).hexdigest()}`.')
        for case in ('present', 'absent'):
            pattern = patterns[article][case]
            expected = text.find(pattern)
            if (case == 'present') != (expected >= 0):
                raise ValueError(f'Invalid {article}/{case} benchmark pattern')
            for name, search in algorithms.items():
                assert search(text, pattern) == expected
                times = [elapsed / number for elapsed in timeit.repeat(
                    lambda: search(text, pattern), number=number, repeat=repeats)]
                medians[article, case, name] = statistics.median(times)
                for repeat, seconds in enumerate(times, 1):
                    rows.append((article, case, name, expected, repeat, number, seconds))
    output.mkdir(parents=True, exist_ok=True)
    with (output / 'search.csv').open('w', encoding='utf-8', newline='') as stream:
        writer = csv.writer(stream)
        writer.writerow(('article', 'pattern_case', 'algorithm', 'match_index', 'repeat', 'calls_per_repeat', 'seconds_per_call'))
        writer.writerows(rows)
    report = ['# Substring-search measurements', '',
              f'Python {platform.python_version()}; {platform.platform()}; {datetime.now(timezone.utc).isoformat()}.', '',
              f'{repeats} timeit repetitions of {number} calls each. Medians below include pattern preprocessing and actual search, but exclude file I/O. Each case uses the same text and pattern for every method. Inputs and fixed patterns are bundled in data/.', '',
              *identities, '', '| Text | Pattern | Boyer–Moore–Horspool (ms) | KMP (ms) | Rabin–Karp (ms) | Fastest |',
              '|---|---|---:|---:|---:|---|']
    for article in ('article1', 'article2'):
        for case in ('present', 'absent'):
            values = {name: medians[article, case, name] for name in algorithms}
            winner = min(values, key=values.get)
            report.append(f'| {article} | {case} | ' + ' | '.join(f'{x * 1000:.4f}' for x in values.values()) + f' | {winner} |')
    report += ['', '## Conclusions', '']
    for article in ('article1', 'article2'):
        scores = {name: statistics.mean(medians[article, case, name] for case in ('present', 'absent')) for name in algorithms}
        winner = min(scores, key=scores.get)
        report.append(f'{article}: {winner} has the lowest mean of the present/absent case medians ({scores[winner] * 1000:.4f} ms).')
    overall = {name: statistics.mean(medians[article, case, name] for article in ('article1', 'article2') for case in ('present', 'absent')) for name in algorithms}
    winner = min(overall, key=overall.get)
    report += [f'Overall: {winner} has the lowest equally weighted mean of the four case medians ({overall[winner] * 1000:.4f} ms).', '',
               'Boyer–Moore–Horspool can skip sections of text; KMP avoids rechecking matched prefixes and has O(n + m) worst-case time. Rabin–Karp updates a rolling hash but must verify matching hashes to avoid false matches. Its small modulus deliberately makes collision handling visible and can increase verification work.',
               'These findings concern the bundled Ukrainian articles and four fixed patterns. Pattern length, match position, repetition, encoding choices, and implementation overhead can change the result. They do not prove a universal ranking.', '',
               'The course calls its shift-table method Boyer–Moore. The implementation here is its bad-character-only Horspool variant, not the full good-suffix version.']
    (output / 'search_report.md').write_text('\n'.join(report) + '\n', encoding='utf-8')
    print(f'Saved {len(rows)} measurements to {output}')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=Path('results'))
    parser.add_argument('--repeats', type=int, default=7)
    parser.add_argument('--number', type=int, default=30)
    args = parser.parse_args()
    if args.repeats < 1 or args.number < 1:
        parser.error('repeats and number must be positive')
    benchmark(args.output, args.repeats, args.number)


if __name__ == '__main__':
    main()
