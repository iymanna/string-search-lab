"""Find all occurrences of a pattern and count character comparisons."""

import argparse
from dataclasses import dataclass
from pathlib import Path


@dataclass
class SearchResult:
    positions: list[int]
    search_comparisons: int
    setup_comparisons: int = 0


def naive_search(text: str, pattern: str) -> SearchResult:
    if not pattern:
        raise ValueError("pattern must not be empty")
    positions = []
    comparisons = 0
    width = len(pattern)

    for start in range(len(text) - width + 1):
        for offset, character in enumerate(pattern):
            comparisons += 1
            if text[start + offset] != character:
                break
        else:
            positions.append(start)

    return SearchResult(positions, comparisons)


def prefix_table(pattern: str) -> tuple[list[int], int]:
    """For each pattern prefix, record its longest proper prefix that is also a suffix."""
    lengths = [0] * len(pattern)
    index = 1
    matched = comparisons = 0
    while index < len(pattern):
        comparisons += 1
        if pattern[index] == pattern[matched]:
            matched += 1
            lengths[index] = matched
            index += 1
        elif matched:
            matched = lengths[matched - 1]
        else:
            index += 1

    return lengths, comparisons


def kmp_search(text: str, pattern: str) -> SearchResult:
    if not pattern:
        raise ValueError("pattern must not be empty")
    if len(pattern) > len(text):
        return SearchResult([], 0)
    lengths, setup_comparisons = prefix_table(pattern)
    positions = []
    index = matched = comparisons = 0
    while index < len(text):
        comparisons += 1
        if text[index] == pattern[matched]:
            index += 1
            matched += 1
            if matched == len(pattern):
                positions.append(index - matched)
                matched = lengths[matched - 1]
        elif matched:
            matched = lengths[matched - 1]
        else:
            index += 1

    return SearchResult(positions, comparisons, setup_comparisons)


def show_comparison(name: str, text: str, pattern: str) -> None:
    naive = naive_search(text, pattern)
    kmp = kmp_search(text, pattern)
    if naive.positions != kmp.positions:
        raise RuntimeError("search algorithms returned different positions")

    print(f"{name} ({len(text)} text characters, {len(pattern)} pattern characters)")
    positions = ", ".join(str(position) for position in naive.positions[:12])
    if len(naive.positions) > 12:
        positions += ", …"
    print(f"Matches ({len(naive.positions)}): {positions or 'none'}")
    print(f"{'Method':<8} {'Setup':>9} {'Search':>9} {'Total':>9}")
    for method, result in (("Naive", naive), ("KMP", kmp)):
        setup, search = result.setup_comparisons, result.search_comparisons
        print(f"{method:<8} {setup:>9,} {search:>9,} {setup + search:>9,}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("demo", help="run two built-in examples")
    find = commands.add_parser("find", help="search a UTF-8 text file")
    find.add_argument("pattern")
    find.add_argument("file", type=Path)
    args = parser.parse_args()

    if args.command == "demo":
        show_comparison("Overlapping matches", "aaaaa", "aaa")
        print()
        show_comparison("Repeated prefix", "a" * 10_000 + "b", "a" * 99 + "b")
    else:
        try:
            text = args.file.read_bytes().decode("utf-8")
            show_comparison(args.file.name, text, args.pattern)
        except (OSError, ValueError) as error:
            parser.exit(1, f"error: {error}\n")


if __name__ == "__main__":
    main()
