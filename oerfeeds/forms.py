import models

from google.appengine.ext.db import djangoforms

class OerFeedForm(djangoforms.ModelForm):
    
    class Meta:
        model = models.OerFeed
        exclude = ('creator',)
