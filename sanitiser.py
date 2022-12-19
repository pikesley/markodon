import re
from pathlib import Path


def unquote(line):
    """Remove the enclosing quotes."""
    if line.startswith('"'):
        line = line[1:]

    if line.endswith('"'):
        line = line[:-1]

    return line


def remove_users(line):
    """Remove @usernames."""
    not_tainted = []
    tokens = line.split(" ")

    for token in tokens:
        if not token.startswith("@"):
            not_tainted.append(token)

    return " ".join(not_tainted).strip()


def remove_urls(line):
    """Remove URLs."""
    return compress(re.sub(r"https?:\/\/[\S]*", "", line))


def remove_newlines(line):
    """Remove embedded newlines."""
    return compress(line.replace("\\n", " "))


def unescape_embedded_quotes(line):
    """Remove embedded quotes."""
    return compress(line.replace('\\"', '"'))


def remove_truncation(line):
    """Remove truncated words."""
    tokens = line.split(" ")
    if tokens[-1].endswith("…"):
        tokens.pop()

    return " ".join(tokens)


def remove_rts(line):
    """Remove `RT`."""
    if line.startswith("RT"):
        return None

    return line


def fix_encodings(line):
    """Replace `&amp;` etc."""
    encodings = {"&amp;": "&", "&lt;": "<", "&gt;": ">"}

    for encoded, plain in encodings.items():
        line = line.replace(encoded, plain)

    return compress(line)


def remove_wordle(line):
    """Remove `Wordle` tweets."""
    if line.startswith("Wordle "):
        return None

    return line


def remove_embedded_quotes_and_friends(line):
    """Safely nuke embedded quotes."""
    tokens = line.split(" ")
    unquoted = []
    quotes_and_ting = ['"', "'", "`", "“", "”", "‘", "’", "*", "_"]
    closing_punctuation = ["?", "!", ",", ".", ":"]

    for token in tokens:
        for symbol in quotes_and_ting:
            if token.startswith(symbol):
                token = token[1:]
            if token.endswith(symbol):
                token = token[:-1]

            token = re.sub(
                rf"(.*)\{symbol}([{''.join(closing_punctuation)}])", "\\1\\2", token
            )

        unquoted.append(token)

    return compress(" ".join(unquoted))


def compress(line):
    """Nuke multiple spaces."""
    return re.sub(r"\s{2,}", " ", line).strip()


def fix_file(in_file, out_file):
    """Fixup a whole file."""
    lines = Path(in_file).read_text(encoding="utf-8").split("\n")
    clean_lines = []
    for line in lines:

        for method in [
            "unquote",
            "unescape_embedded_quotes",
            "remove_newlines",
            "remove_embedded_quotes_and_friends",
            "remove_rts",
            "remove_wordle",
            "remove_users",
            "remove_urls",
            "remove_truncation",
            "fix_encodings",
        ]:
            if line:
                line = globals()[method](line)

        if line:
            clean_lines.append(line)

    Path(out_file).write_text("\n".join(clean_lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    fix_file("raw-tweets.txt", "tweets.txt")
