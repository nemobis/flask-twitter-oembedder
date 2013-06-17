import requests
from requests_oauthlib import OAuth1
from flask import Markup

class TwitterOEmbedder(object):
    
    def __init__(self, app=None, cache=None, debug=False):
        if app is not None and cache is not None:
            self.init(app, cache, debug)
    def init(self, app, cache, debug=False):
        @app.context_processor
        def tweet_processor():
            @cache.memoize(timeout=60*60*24*356)
            def oembed_tweet(tweet_id):
                auth = OAuth1(app.config['TWITTER_CONSUMER_KEY'],
                              app.config['TWITTER_CONSUMER_SECRET'],
                              app.config['TWITTER_ACCESS_TOKEN'],
                              app.config['TWITTER_TOKEN_SECRET'])
                url = 'https://api.twitter.com/1.1/statuses/oembed.json'
                payload = {'id':tweet_id}
                r = requests.get(url, params=payload, auth=auth)
                try:
                    tweet_html = Markup(r.json()[u'html'])
                except KeyError as e:
                    if debug:
                        raise e
                    else:
                        return ''
                return tweet_html
            return dict(oembed_tweet=oembed_tweet)