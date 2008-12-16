import cgi
import logging

import simplejson
import feedparser

from support import render_template
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import login_required
from google.appengine.api import users
from google.appengine.api import urlfetch

import models
import forms

class Opml(webapp.RequestHandler):
    """Render the available feeds as an OPML file."""

    def get(self):

        feeds = models.OerFeed.gql("ORDER BY updated DESC")
        if feeds.count() > 0:
            lastModified = feeds[0].updated
        else:
            lastModified = ""
        
        self.response.headers['Content-type'] = 'text/x-opml'
        self.response.out.write(
            render_template('feeds.opml', 
                            dict(feeds=feeds,
                                 lastModified=lastModified))
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
            self.error(403)

        # get the item we're editing, if that's what we're doing
        instance = self._get_existing(key)

        # make sure we're allowed to edit this
        if instance is not None and not(users.is_current_user_admin()) and \
                instance.creator != users.get_current_user():
            self.error(403)
            
        data = forms.OerFeedForm(instance = instance,
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


    def _get_existing(self, key):

        return models.OerFeed.get(db.Key.from_path('OerFeed', int(key)))

    @login_required
    def get(self, key=None):
        
        feed = self._get_existing(key)

        if not(users.is_current_user_admin()) and \
                feed.creator != users.get_current_user():
            self.error(403)

        self.response.out.write(
            render_template('delete.html', 
                            dict(feed=feed), 
                            self.request)
            )

    def post(self, key=None):

        # make sure the user is currently logged in
        if users.get_current_user() is None:
            self.error(403)

        # get the item we're deleting
        feed = self._get_existing(key)

        # make sure we're allowed to delete this
        if not(users.is_current_user_admin()) and \
                feed.creator != users.get_current_user():
            self.error(403)
            
        # see if the user confirmed
        if self.request.get('confirm', 'Cancel') == 'Delete':
            feed.delete()

        self.redirect('/userfeeds/')


class UserFeeds(webapp.RequestHandler):

    @login_required
    def get(self):

        feeds = models.OerFeed.gql("WHERE creator = :user",
                                   user = users.get_current_user())

        self.response.out.write(
            render_template('userfeeds.html', dict(feeds = feeds), 
                            self.request)
            )

class Scrape(webapp.RequestHandler):

    def get(self):

        result = {}

        result['url'] = self.request.get('feed_url', None)
        if result['url'] is not None:

            feed_contents = urlfetch.fetch(result['url'])
            doc = feedparser.parse(feed_contents.content)
            logging.info(doc)
            # result['content-type'] = feed.headers['content-type'].split(';')[0]
            result['title'] = doc.feed.title
            result['format'] = doc.feed.info_detail.type
        else:
            result['content-type'] = ''

        self.response.headers['content-type'] = 'text/plain'
        self.response.out.write( simplejson.dumps(result) )

