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
    return remove_thing(line, "@")


def nuke_urls(line):
    """Remove URLs."""
    return remove_thing(line, "http")


def remove_thing(line, pattern):
    """Remove token that starts with `pattern`."""
    not_tainted = []
    tokens = line.split(" ")

    for token in tokens:
        if not token.startswith(pattern):
            not_tainted.append(token)

    return " ".join(not_tainted)


def no_newlines(line):
    """Remove embedded newlines."""
    return line.replace("\\n", " ")


def unescape_embedded_quotes(line):
    """Remove embedded quotes."""
    return line.replace('\\"', '"')


def detruncate(line):
    """Remove truncated words."""
    tokens = line.split(" ")
    if tokens[-1].endswith("…"):
        tokens.pop()

    return " ".join(tokens)


def excise_rts(line):
    """Remove `RT`."""
    if line.startswith("RT"):
        return None

    return line


def fix_encodeds(line):
    """Replace `&amp;` etc."""
    encodings = {"&amp;": "&", "&lt;": "<", "&gt;": ">"}

    for encoded, plain in encodings.items():
        line = line.replace(encoded, plain)

    return line


def fix_file(in_file, out_file):
    """Fixup a whole file."""
    lines = Path(in_file).read_text().split("\n")
    clean_lines = []
    for line in lines:
        line = unquote(line)
        line = remove_users(line)
        line = nuke_urls(line)
        line = no_newlines(line)
        line = unescape_embedded_quotes(line)
        line = detruncate(line)
        line = fix_encodeds(line)
        line = excise_rts(line)

        if line:
            clean_lines.append(line)

    Path(out_file).write_text("\n".join(clean_lines) + "\n")


if __name__ == "__main__":
    fix_file("raw-tweets.txt", "tweets.txt")
