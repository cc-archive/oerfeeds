import cgi

from support import render_template
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import login_required
from google.appengine.api import users

import models
import forms

class Opml(webapp.RequestHandler):
    """Render the available feeds as an OPML file."""

    def get(self):

        feeds = model.OerFeed.all()

        # XXX
        self.response.headers['Content-type'] = 'application/opml'
        self.response.out.write(
            render_template('feeds.opml', dict(feeds=feeds))
            )


class Index(webapp.RequestHandler):
    def get(self):

        recent_feeds = models.OerFeed.all()[:10]

        self.response.out.write(
            render_template('index.html', dict(feeds = recent_feeds), 
                            self.request)
            )


class AddOrEdit(webapp.RequestHandler):

    def _get_existing(self, key):

        if key is not None:
            return models.OerFeed.get(db.Key.from_path('OerFeed', int(key)))

        return None

    @login_required
    def get(self, key=None):
        
        feed = self._get_existing(key)
        form = forms.OerFeedForm(instance = feed)

        self.response.out.write(
            render_template('add.html', 
                            dict(form=form,
                                 feed=feed), 
                            self.request)
            )

    def post(self, key=None):

        # make sure the user is currently logged in
        if users.get_current_user() is None:
            self.redirect('/')

        data = forms.OerFeedForm(instance = self._get_existing(key),
                                 data=self.request.POST)

        if data.is_valid():
            # Save the data, and redirect to the view page
            entity = data.save(commit=False)
            entity.creator = users.get_current_user()
            entity.put()

            self.redirect('/')

        else:
            # An error occured; redisplay the form
            self.response.out.write(
                render_template('add.html', dict(form=data), self.request))


class Delete(webapp.RequestHandler):

    @login_required
    def get(self, key):

        # get the specified feed

        # make sure the logged in user "owns" it

        pass

    def post(self, key):
        pass


class UserFeeds(webapp.RequestHandler):

    @login_required
    def get(self):

        feeds = models.OerFeed.gql("WHERE creator = :user",
                                   user = users.get_current_user())

        self.response.out.write(
            render_template('userfeeds.html', dict(feeds = feeds), 
                            self.request)
            )

