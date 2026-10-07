# Tab Expansion to Minimum Width

Expands tab characters to the minimum number of spaces required to reach the next multiple of the configured tab width on each line.

```python
from tab_expansion_to_minimum_width import expand_tabs

print(repr(expand_tabs("a\tb\tcd", tab_width=4)))
# 'a   b   cd  '
```

## Why this exists

Mixing tabs and spaces in source files breaks alignment when viewers disagree on tab width. Converting tabs to spaces using the standard "advance to next tab stop" rule — rather than a fixed 1:1 replacement or a naive 8-space blanket — preserves the original visual layout under any tab width setting. This library is that single rule, with no dependencies, callable on any string.

The trade-off: the function is line-aware but otherwise character-blind. It does not understand CRLF line endings specially; `\r` occupies one column just like a printable character. This keeps behaviour deterministic on arbitrary text, at the cost of not "fixing" Windows line endings for you.

## Edge case you will hit

`\r` is treated as a one-column character, not a carriage return that resets the column. If your text contains `\r\n`, the `\r` will shift the tab stop by one before the `\n` resets it. Strip `\r` first if you need classic CRLF handling.

## Exported names

- `expand_tabs(text, tab_width=8) -> str` — expands `\t` characters in `text` using minimum-width column advancement with the given positive integer `tab_width`.
