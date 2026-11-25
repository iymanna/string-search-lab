from unittest import TestCase

from search import kmp_search, naive_search, prefix_table


class SearchTests(TestCase):
    def test_overlapping_matches(self):
        for search in (naive_search, kmp_search):
            with self.subTest(search=search.__name__):
                self.assertEqual(search("aaaaa", "aaa").positions, [0, 1, 2])
                self.assertEqual(search("火车火车火", "火车火").positions, [0, 2])

    def test_boundaries(self):
        for search in (naive_search, kmp_search):
            with self.subTest(search=search.__name__):
                self.assertEqual(search("", "a").positions, [])
                self.assertEqual(search("a", "ab").positions, [])
                self.assertEqual(search("abc", "z").positions, [])
                self.assertEqual(search("abc", "abc").positions, [0])
                with self.assertRaisesRegex(ValueError, "empty"):
                    search("abc", "")

    def test_prefix_lengths(self):
        self.assertEqual(prefix_table("ababaca")[0], [0, 0, 1, 2, 3, 0, 1])

    def test_comparison_counts(self):
        naive = naive_search("aaaaa", "aaa")
        kmp = kmp_search("aaaaa", "aaa")
        self.assertEqual(naive.search_comparisons, 9)
        self.assertEqual(kmp.search_comparisons, 5)
        self.assertEqual(kmp.setup_comparisons, 2)
