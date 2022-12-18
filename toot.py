from pathlib import Path

import yaml
from markovchain.text import MarkovText
from mastodon import Mastodon

conf = yaml.safe_load(Path("conf.yaml").read_text())
markov = MarkovText()
s = Path("tweets.txt").read_text()

markov.data(s)

toot = ""
while len(toot) < conf["min-toot-length"]:
    toot = markov(max_length=32)

print(f"Tooting: {toot}")

mastodon = Mastodon(api_base_url=conf["server"], access_token=conf["token"])
mastodon.toot(toot)
