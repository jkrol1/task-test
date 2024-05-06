from command.grep.context import PatternMatchingOptions
from match import BinaryPatternMatcher, MatchPosition, TextPatternMatcher


def test_binary_pattern_matcher_search() -> None:
    options = PatternMatchingOptions(
        invert_match=False, word_regexp=False, ignore_case=False
    )
    pattern_matcher = BinaryPatternMatcher([r"\xF0\x9F\x91\x8D"], options)
    result = pattern_matcher.search(
        b"\xF0\x9F\x91\x8D \xF0\x9F\x91\x8D \xF0\x9F\x98\x8A"
    )
    assert result == MatchPosition(0, 4)


def test_binary_pattern_matcher_search_invert() -> None:
    options = PatternMatchingOptions(
        invert_match=True, word_regexp=False, ignore_case=False
    )
    pattern_matcher = BinaryPatternMatcher([r"\xF0\x9F\x91\x8D"], options)
    result = pattern_matcher.search(
        b"\xF0\x9F\x91\x8D \xF0\x9F\x91\x8D \xF0\x9F\x98\x8A"
    )
    assert not result


def test_binary_pattern_matcher_match() -> None:
    options = PatternMatchingOptions(
        invert_match=False, word_regexp=False, ignore_case=False
    )
    pattern_matcher = BinaryPatternMatcher([r"\xF0\x9F\x91\x8D"], options)
    result = pattern_matcher.match(
        b"\xF0\x9F\x91\x8D \xF0\x9F\x91\x8D \xF0\x9F\x98\x8A"
    )
    assert result == [MatchPosition(0, 4)]


def test_binary_pattern_matcher_match_invert() -> None:
    options = PatternMatchingOptions(
        invert_match=True, word_regexp=False, ignore_case=False
    )
    pattern_matcher = BinaryPatternMatcher([r"\xF0\x9F\x91\x8D"], options)
    result = pattern_matcher.match(
        b"\xF0\x9F\x91\x8D \xF0\x9F\x91\x8D \xF0\x9F\x98\x8A"
    )
    assert not result


def test_text_pattern_matcher_search() -> None:
    options = PatternMatchingOptions(
        invert_match=False, word_regexp=False, ignore_case=False
    )
    pattern_matcher = TextPatternMatcher(
        [r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"], options
    )
    result = pattern_matcher.search(
        "test test@gmail.com test test test2@wp.pl"
    )
    assert result == MatchPosition(5, 19)


def test_text_pattern_matcher_search_invert() -> None:
    options = PatternMatchingOptions(
        invert_match=True, word_regexp=False, ignore_case=False
    )
    pattern_matcher = TextPatternMatcher(
        [r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"], options
    )
    result = pattern_matcher.search(
        "test test@gmail.com test test test2@wp.pl"
    )
    assert not result


def test_text_pattern_matcher_match() -> None:
    options = PatternMatchingOptions(
        invert_match=False, word_regexp=False, ignore_case=False
    )
    pattern_matcher = TextPatternMatcher(
        [r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"], options
    )
    result = pattern_matcher.match("test test@gmail.com test test test2@wp.pl")
    assert result == [MatchPosition(5, 19), MatchPosition(30, 41)]


def test_text_pattern_matcher_match_invert() -> None:
    options = PatternMatchingOptions(
        invert_match=True, word_regexp=False, ignore_case=False
    )
    pattern_matcher = TextPatternMatcher(
        [r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"], options
    )
    result = pattern_matcher.match("test test@gmail.com test test test2@wp.pl")
    assert not result


def test_text_pattern_matcher_match_word_regexp() -> None:
    options = PatternMatchingOptions(
        invert_match=False, word_regexp=True, ignore_case=False
    )
    pattern_matcher = TextPatternMatcher([r"test"], options)
    result = pattern_matcher.match("test2@wp.pl test")
    assert result == [MatchPosition(12, 16)]


def test_text_pattern_matcher_match_ignore_case() -> None:
    options = PatternMatchingOptions(
        invert_match=False, word_regexp=False, ignore_case=True
    )
    pattern_matcher = TextPatternMatcher([r"test"], options)
    result = pattern_matcher.match("test TesT TEST")
    assert result == [
        MatchPosition(0, 4),
        MatchPosition(5, 9),
        MatchPosition(10, 14),
    ]
