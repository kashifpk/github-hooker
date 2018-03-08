"""
Handle github webhooks
======================

Handles incoming requests from github when webhooks are activated. Allows for performing actions
easily on webhook events.
"""

import subprocess
from bottle import run, post, request
from logger import get_configured_logger

log = get_configured_logger(__name__, 'github_webhook.log')

REPO_FOLDER = '/root/tf-frontend'
WEBROOT = '/var/www/html'


def pull_code(repo_path):
    log.info("Pulling latest code...")
    try:
        subprocess.run("cd /root/tf-frontend; git pull origin master", shell=True, check=True)
    except subprocess.CalledProcessError as exp:
        log.error("Error pulling updates, aborting :-(")
        log.error(exp)
        return False
    else:
        log.info("Done!")

    return True


def deploy_to_web(repo_path, web_path):
    log.info("Copying to web root: %s", web_path)
    try:
        subprocess.run("cd {}/dist/; cp -r * {}/".format(repo_path, web_path), shell=True, check=True)
    except subprocess.CalledProcessError as exp:
        log.error("Error copying to web root, aborting :-(")
        log.error(exp)
        return False
    else:
        log.info("Done!")

    # log.info("Restarting web server")
    # try:
    #     subprocess.run("service apache2 restart", shell=True, check=True)
    # except subprocess.CalledProcessError as exp:
    #     log.error("Error restarting web server, aborting :-(")
    #     log.error(exp)
    #     return False

    return True


@post('/repo_pushed')  # or @route('/login', method='POST')
def handle_repo_push_event():
    event = request.headers.get('X-GitHub-Event')  # pylint: disable=E1101
    log.info("Event: " + event)

    if 'ping' == event:
        log.info("Got ping event")
        return

    elif 'push' == event:
        
        branch = request.json.get('ref').split('/')[-1]
        
        if 'master' == branch:
            log.info("changes pushed to master branch")
            
            pusher = request.json.get('pusher')
            log.info("Pushed by %s (%s)", pusher['name'], pusher['email'])

            hc = request.json.get('head_commit')
            log.info("Head commit: %s", hc['id'])
            log.info("  By: %s (%s)", hc['committer']['name'], hc['committer']['email'])
            log.info("  on: %s", hc['timestamp'])
            log.info("  %s", hc['message'])

            pull_code(REPO_FOLDER)
            deploy_to_web(REPO_FOLDER, WEBROOT)

run(host='0.0.0.0', port=9999, debug=True)
