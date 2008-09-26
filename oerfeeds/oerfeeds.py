import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

import views

application = webapp.WSGIApplication(
    [('/', views.Index),
     ('/add/', views.AddOrEdit),
     ('/edit/(.+)/', views.AddOrEdit),
     ('/delete/(.+)/', views.Delete),
     ('/userfeeds/', views.UserFeeds),
     ('/feeds.opml', views.Opml),
     ],
    debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()
