import unittest

from tab_expansion_to_minimum_width import expand_tabs


class ExpandTabsTests(unittest.TestCase):
    def test_no_tabs_unchanged(self):
        self.assertEqual(expand_tabs("hello world"), "hello world")

    def test_empty_string(self):
        self.assertEqual(expand_tabs(""), "")

    def test_tab_at_column_zero(self):
        self.assertEqual(expand_tabs("\t"), " " * 8)

    def test_tab_at_column_zero_custom_width(self):
        self.assertEqual(expand_tabs("\t", tab_width=4), " " * 4)

    def test_tab_at_last_column_before_boundary(self):
        # column 7 -> next multiple of 8 is 8, so 1 space
        self.assertEqual(expand_tabs("x" * 7 + "\t"), "x" * 7 + " ")

    def test_tab_at_column_zero_after_seven(self):
        # column 7 with tab_width=4: next multiple is 8, so 1 space
        self.assertEqual(expand_tabs("x" * 7 + "\t", tab_width=4), "x" * 7 + " ")

    def test_two_consecutive_tabs(self):
        # first tab: col 0 -> 8 (8 spaces), second tab: col 8 -> 16 (8 spaces)
        self.assertEqual(expand_tabs("\t\t"), " " * 16)

    def test_column_resets_per_line(self):
        self.assertEqual(expand_tabs("ab\t\n\tx"), "ab      \n        x")

    def test_carriage_return_treated_as_one_column(self):
        # \r is an ordinary character: col 0 '\r' -> col 1, then tab -> col 8 (7 spaces)
        self.assertEqual(expand_tabs("\r\t"), "\r" + " " * 7)

    def test_mixed_text_and_tabs(self):
        self.assertEqual(
            expand_tabs("a\tb\tcd\te", tab_width=4),
            "a   b   cd  e",
        )

    def test_tab_width_one(self):
        self.assertEqual(expand_tabs("\t\t\t", tab_width=1), "   ")

    def test_negative_tab_width_raises(self):
        with self.assertRaises(ValueError):
            expand_tabs("\t", tab_width=-1)

    def test_zero_tab_width_raises(self):
        with self.assertRaises(ValueError):
            expand_tabs("\t", tab_width=0)

    def test_non_string_text_raises(self):
        with self.assertRaises(TypeError):
            expand_tabs(123)

    def test_bool_tab_width_raises(self):
        with self.assertRaises(TypeError):
            expand_tabs("\t", tab_width=True)

    def test_only_tabs_expanded_other_control_passed_through(self):
        # \x00 is a NUL byte: treated as one column, not expanded
        self.assertEqual(expand_tabs("\x00\t", tab_width=8), "\x00" + " " * 7)


if __name__ == "__main__":
    unittest.main()
