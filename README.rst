github-hooker
=============

Easily handle github hooks. This package allows easily handling github webhooks by running a simple bottle
webserver to handle requests coming from github. All it requires is a module containing functions with
predefined names to handle the github event transmitted via webhook.

Example:

.. code:: bash

    github_hooker -c config.json -m github_actions.py
