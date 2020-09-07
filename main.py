import requests
import os
import json
import sys


def actionColor(status):
    """
    Get a action color based on the workflow status.
    """

    if status == 'success':
        return 'good'
    elif status == 'failure':
        return 'danger'

    return 'warning'


def actionStatus(status):
    """
    Get a transformed status based on the workflow status.
    """

    if status == 'success':
        return 'passed'
    elif status == 'failure':
        return 'failed'

    return 'passed with warnings'


def actionEmoji(status):
    """
    Get an emoji based on the workflow status.
    """

    if status == 'success':
        return ':sunglasses:'
    elif status == 'failure':
        return ':worried:'

    return ':zipper_mouth_face:'


def notify_slack(job_status, notify_when):
    url = os.getenv('SLACK_WEBHOOK_URL')
    workflow = os.getenv('GITHUB_WORKFLOW')
    repo = os.getenv('GITHUB_REPOSITORY')
    branch = os.getenv('GITHUB_REF')
    commit = os.getenv('GITHUB_SHA')

    commit_url = f'https://github.com/{repo}/commit/{commit}'
    repo_url = f'https://github.com/{repo}/tree/{branch}'

    color = actionColor(job_status)
    status_message = actionStatus(job_status)
    emoji = actionEmoji(job_status)

    message = f'{emoji} {workflow} {status_message} in <{repo_url}|{repo}@{branch}> on <{commit_url}|{commit[:7]}>.'

    payload = {
        'attachments': [
            {
                'text': message,
                'fallback': 'New Github Action Run',
                'pretext': 'New Github Action Run',
                'color': color,
                'mrkdwn_in': ['text'],
                'footer': 'Developed by <https://www.ravsam.in|RavSam>',
            }
        ]
    }

    payload = json.dumps(payload)

    headers = {'Content-Type': 'application/json'}

    if notify_when is None:
        notify_when = 'success,failure,warnings'

    if job_status in notify_when and not testing:
        requests.post(url, data=payload, headers=headers)


def main():
    job_status = os.getenv('INPUT_STATUS')
    notify_when = json.loads(os.getenv('INPUT_NOTIFY_WHEN'))
    notify_slack(job_status, notify_when)


if __name__ == '__main__':
    try:
        testing = True if sys.argv[1] == '--test' else False
    except IndexError as e:
        testing = False

    main()
