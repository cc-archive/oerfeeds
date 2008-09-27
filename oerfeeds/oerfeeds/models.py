from google.appengine.ext import db

FEED_TYPES = ('RSS', 'Atom', 'OPML', 'OAI-PMH',)

class OerFeed(db.Model):
    creator = db.UserProperty()

    url = db.LinkProperty()
    title = db.StringProperty()
    format = db.StringProperty(
        choices=FEED_TYPES)

    created = db.DateTimeProperty(auto_now_add=True)
    updated = db.DateTimeProperty(auto_now=True)
