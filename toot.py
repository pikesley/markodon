from pathlib import Path

import yaml
from mastodon import Mastodon

from toot_maker import make_toot

conf = yaml.safe_load(Path("conf.yaml").read_text(encoding="utf-8"))


def send_toot(toot):
    """Send a toot."""
    mastodon = Mastodon(api_base_url=conf["server"], access_token=conf["token"])

    print(f"Tooting: {toot}")
    mastodon.toot(toot)


if __name__ == "__main__":
    send_toot(make_toot())
