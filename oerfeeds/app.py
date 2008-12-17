import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from oerfeeds import views

application = webapp.WSGIApplication(
    [('/', views.Index),
     ('/h/details', views.Help),
     ('/add/', views.AddOrEdit),
     ('/edit/(.+)/', views.AddOrEdit),
     ('/delete/(.+)/', views.Delete),
     ('/userfeeds/', views.UserFeeds),
     ('/feeds/', views.Feeds),
     ('/feeds/opml', views.Opml),
     ('/scrape', views.Scrape),
     ],
    debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()
