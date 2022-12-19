# Markodon

_Force your old tweets through a [Markov Chain](https://en.wikipedia.org/wiki/Markov_chain) like coffee through a civet_

## Install this

You'll need Python 3 (I built it with `3.10`, but I now have it working with `3.6` elsewhere)

```
git clone https://github.com/pikesley/markodon
cd markodon
make install
```
## Prepare your tweets

### Download your Twitter archive

If that's still a thing by the time you're reading this

### Prepare the data

Unpack your archive

```
unzip twitter-datestamp-long-alphanumeric-string.zip
cd data
```

Extract just the tweets from the JSON:

```
make extract
```

Copy the tweets to here:

```
cp /path/to/raw-tweets.txt .
```

Sanitise the tweets file:

```
make sanitise
```

This does the following to the archive:

* Removes the enclosing quotes from each tweet
* Removes embedded newlines
* Removes embedded quotes and so on (`'`, `"`, `*` etc)
* Removes all `RT` tweets
* Removes all `wordle` tweets
* Removes all `@username` words
* Removes all URLs
* Removes any truncated words from the end of a tweet
* Replaces HTML-encoded strings (`&amp;` etc) with their plain-text equivalents

So now you have a cleaned, sanitised list of your tweets at `tweets.txt`.

## Get set up

You need to create a Mastodon application, with the `write` scope. Once you've done this, you just need `Your acccess token` (you can safely ignore all the Oauth stuff)

You need the conf-file:

```
cp conf-example.yaml conf.yaml
```

And then fill in:

* Your `server` URL (e.g. `https://mastoodn.me.uk`)
* Your `token` from your application
* Optionally, change the `min-toot-length`

## Send a toot

And now, to generate and send a toot,

```
make toot
```

## Hacking on it

If you want to play with the (hastily-written over a weekend) code, there's a Docker image

```
make build
make run
```

To run the tests:

```
make all
```
