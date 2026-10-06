def expand_tabs(text, tab_width=8):
    """Expand tab characters into spaces using minimum-width column advancement.

    For each tab, the number of replacement spaces is the distance from the
    current visual column to the next multiple of ``tab_width``. This matches
    the behaviour of Unix ``expand`` and most editors' default tab handling:
    a tab at column 0 with ``tab_width=8`` becomes 8 spaces, but a tab at
    column 7 becomes a single space.

    Design decisions:

    * Column counting is per line and resets at every ``\n``. ``\r`` is treated
      as an ordinary character occupying one column, which keeps the function
      deterministic on arbitrary text and avoids heuristic CRLF handling that
      would surprise callers feeding raw binary-ish strings.
    * ``tab_width`` must be a positive integer. A zero or negative width makes
      "next multiple of N" undefined; we reject it eagerly rather than picking
      an arbitrary fallback.
    * Non-string input raises ``TypeError`` so callers learn the contract
      early instead of getting a confusing ``AttributeError`` deep in the loop.
    * Only ``\t`` is expanded. Other control characters are passed through
      unchanged and still advance the column by one, which is the least
      surprising rule for text that contains them.
    """
    if not isinstance(text, str):
        raise TypeError("text must be str")
    if not isinstance(tab_width, int) or isinstance(tab_width, bool):
        raise TypeError("tab_width must be int")
    if tab_width <= 0:
        raise ValueError("tab_width must be positive")

    out = []
    column = 0
    for ch in text:
        if ch == "\t":
            spaces = tab_width - (column % tab_width)
            out.append(" " * spaces)
            column += spaces
        elif ch == "\n":
            out.append(ch)
            column = 0
        else:
            out.append(ch)
            column += 1
    return "".join(out)
