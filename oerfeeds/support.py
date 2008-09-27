import os
import logging

from google.appengine.ext.webapp import template
from google.appengine.api import users

def render_template(template_path, template_dict, request=None):
    """Resolve the template path in our templates directory and return 
    the rendered version."""

    if request is not None:
        # add the login/logout URLs to the context
        template_dict.update(
            dict(login_url = users.create_login_url(request.path),
                 logout_url = users.create_logout_url(request.path),
                 user = users.get_current_user()
                 )
            )

    return template.render(
        os.path.join(os.path.dirname(__file__), 'templates', template_path),
        template_dict)


