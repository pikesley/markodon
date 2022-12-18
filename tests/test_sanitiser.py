from pathlib import Path

from sanitiser import (detruncate, excise_rts, fix_encodeds, fix_file,
                       no_newlines, nuke_urls, remove_users,
                       unescape_embedded_quotes, unquote)


def test_unquote():
    assert unquote('"some line"') == "some line"
    assert unquote("bare line") == "bare line"


def test_remove_users():
    assert remove_users("nothing here") == "nothing here"
    assert remove_users("@remove_this keep_this") == "keep_this"
    assert remove_users("@remove_this retain these @nuke_this") == "retain these"


def test_nuke_urls():
    assert nuke_urls("some text") == "some text"
    assert (
        nuke_urls("this is ok https://some.thing so is this") == "this is ok so is this"
    )


def test_no_newlines():
    assert no_newlines("this is fine") == ("this is fine")
    assert no_newlines("""this should all\\nbe one line""") == (
        "this should all be one line"
    )


def test_unescape_embedded_quotes():
    assert unescape_embedded_quotes("this one's OK") == "this one's OK"
    assert (
        unescape_embedded_quotes("""this has \\"embedded\\" quotes""")
        == 'this has "embedded" quotes'
    )


def test_detruncate():
    assert detruncate("yeah fine") == "yeah fine"
    assert detruncate("not the last wor…") == "not the last"


def test_excise_rts():
    assert excise_rts("nothing doing") == "nothing doing"
    assert excise_rts("RT some retweet") == None


def test_fix_encodeds():
    assert fix_encodeds("plain old line") == "plain old line"
    assert fix_encodeds("S&amp;M") == "S&M"
    assert fix_encodeds("&lt;foo&gt; &amp; &lt;bar&gt;") == "<foo> & <bar>"


def test_fix_file():
    fix_file("tests/fixtures/tweets.txt", "/tmp/tweets.txt")

    actual = Path("/tmp/tweets.txt").read_text()
    expected = Path("tests/fixtures/cleaned-tweets.txt").read_text()

    assert actual == expected
