github-hooker
=============

Easily handle github hooks. This package allows easily handling github webhooks by running a simple bottle
webserver to handle requests coming from github. All it requires is a module containing functions with
predefined names to handle the github event transmitted via webhook.

The webhook at Github should be configured to send event data as JSON and not as url form encoded.

Example:

.. code:: bash

    github_hooker -c config.json -m github_actions.py


Config file needs to contain host, port and url_path parameters. See config.json under example folder.
The module file should define functions for handling github events. Event handler functions accept a
single parameter which is a `request <https://bottlepy.org/docs/dev/api.html#the-request-object>`_
object.

Example of a function to handle repository pushed event:

.. code:: python

    def on_event_push(request):

        branch = request.json.get('ref').split('/')[-1]
    
        if 'master' == branch:
            print("changes pushed to master branch")
    
            pusher = request.json.get('pusher')
            print("Pushed by {} ({})".format(pusher['name'], pusher['email']))
    
            hc = request.json.get('head_commit')
            print("Head commit: %s" % hc['id'])
            print("  By: %s (%s)" % (hc['committer']['name'], hc['committer']['email']))
            print("  on: %s" % hc['timestamp'])
            print("  %s" % hc['message'])
