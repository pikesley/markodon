from pathlib import Path

from sanitiser import (
    fix_encodings,
    fix_file,
    remove_embedded_quotes_and_friends,
    remove_newlines,
    remove_rts,
    remove_truncation,
    remove_urls,
    remove_users,
    remove_wordle,
    unescape_embedded_quotes,
    unquote,
)


def test_unquote():
    """Test unquoting."""
    assert unquote('"some line"') == "some line"
    assert unquote("bare line") == "bare line"


def test_remove_users():
    """Test removing users."""
    assert remove_users("nothing here") == "nothing here"
    assert remove_users("@remove_this keep_this") == "keep_this"
    assert remove_users("@remove_this retain these @nuke_this") == "retain these"


def test_remove_urls():
    """Test removing URLs."""
    assert remove_urls("some text") == "some text"
    assert (
        remove_urls("this is ok https://some.thing so is this")
        == "this is ok so is this"
    )
    assert (
        remove_urls(
            "Use the API, they said. It’ll be fun, they said.  https://t.co/FemQZJmcFp"
        )
        == "Use the API, they said. It’ll be fun, they said."
    )
    assert (
        remove_urls("http://t.co/fdsa some text 👌https://t.co/x8CCGBiEoj")
        == "some text 👌"
    )


def test_remove_newlines():
    """Test removing newlines."""
    assert remove_newlines("this is fine") == ("this is fine")
    assert remove_newlines("""this should all\\nbe one line""") == (
        "this should all be one line"
    )


def test_unescape_embedded_quotes():
    """Test unescaping embedded quotes."""
    assert unescape_embedded_quotes("this one's OK") == "this one's OK"
    assert (
        unescape_embedded_quotes("""this has \\"embedded\\" quotes""")
        == 'this has "embedded" quotes'
    )


def test_remove_truncation():
    """Test removing truncated words."""
    assert remove_truncation("yeah fine") == "yeah fine"
    assert remove_truncation("not the last wor…") == "not the last"


def test_remove_rts():
    """Test removing retweets."""
    assert remove_rts("nothing doing") == "nothing doing"
    assert remove_rts("RT some retweet") is None


def test_fix_encodings():
    """Test fixing encodings."""
    assert fix_encodings("plain old line") == "plain old line"
    assert fix_encodings("S&amp;M") == "S&M"
    assert fix_encodings("&lt;foo&gt; &amp; &lt;bar&gt;") == "<foo> & <bar>"


def test_remove_wordle():
    """Test removing wordle tweets."""
    assert remove_wordle("regular tweet") == "regular tweet"
    assert remove_wordle("Wordle 508 3/6  ⬛🟨⬛🟨⬛ ⬛⬛🟨🟨🟨 🟩🟩🟩🟩🟩\n") is None


def test_remove_embedded_quotes_and_friends():
    """Test removing embedded quotes and friends."""
    assert remove_embedded_quotes_and_friends("just a line") == "just a line"
    assert remove_embedded_quotes_and_friends("this isn't bad") == "this isn't bad"
    assert (
        remove_embedded_quotes_and_friends("""these "quotes" should be removed""")
        == "these quotes should be removed"
    )
    assert remove_embedded_quotes_and_friends("these 'should' go") == "these should go"
    assert (
        remove_embedded_quotes_and_friends("*goes to *is confused")
        == "goes to is confused"
    )
    assert remove_embedded_quotes_and_friends("Wait, already*?") == "Wait, already?"


def test_fix_file():
    """Test fixing a whole file."""
    fix_file("tests/fixtures/messy-tweets.txt", "/tmp/tweets.txt")

    actual = Path("/tmp/tweets.txt").read_text(encoding="utf-8")
    expected = Path("tests/fixtures/cleaned-tweets.txt").read_text(encoding="utf-8")

    assert actual == expected
