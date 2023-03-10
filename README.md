# Markodon

_Force your old tweets through a [Markov Chain](https://en.wikipedia.org/wiki/Markov_chain) like coffee through a civet_

It's [spouting nonsense on Mastodon](https://mastodon.me.uk/@pikesley_ebooks) as you read this

## Install this

```
git clone https://github.com/pikesley/markodon
cd markodon
export MARKODON=$(pwd)
make install
```

You'll need Python 3 (I built it with `3.10`, but I now have it working with `3.8` elsewhere)

## Prepare your tweets

### Download your Twitter archive

If that's still a thing by the time you're reading this

### Prepare the data

Unpack your archive and copy the JSON to here:

```
cd /tmp/
unzip /path/to/twitter-datestamp-long-alphanumeric-string.zip
cp data/tweets.js ${MARKODON}/
cd ${MARKODON}/
```

Extract just the tweets from the JSON:

```
make extract
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

* Your `server` URL (e.g. `https://mastodon.me.uk`)
* Your `token` from your application
* Optionally, the `max-toot-length`

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
