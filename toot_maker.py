from pathlib import Path

import markovify
import yaml

conf = yaml.safe_load(Path("conf.yaml").read_text(encoding="utf-8"))
max_length = conf["max-toot-length"] if "max-toot-length" in conf else 300


def make_toot():
    """Make a toot."""
    # we could serialise this, but it's *extremely* quick to generate, so ¯\_(ツ)_/¯
    text_model = markovify.Text(Path("tweets.txt").read_text(encoding="utf-8"))
    return text_model.make_short_sentence(max_length)


if __name__ == "__main__":
    print(make_toot())
