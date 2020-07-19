import requests
import os
import json


def action_color(status):
    """
    Get a action color based on the workflow status.
    """

    if status == 'success':
        return 'good'
    elif status == 'failure':
        return 'danger'

    return 'warning'


def action_status(status):
    """
    Get a transformed status based on the workflow status.
    """

    if status == 'success':
        return 'passed'
    elif status == 'failure':
        return 'failed'

    return 'passed with warnings'


def action_emoji(status):
    """
    Get an emoji based on the workflow status.
    """

    if status == 'success':
        return ':sunglasses:'
    elif status == 'failure':
        return ':worried:'

    return ':zipper_mouth_face:'


def notify_slack(job_status):
    url = os.environ.get('SLACK_WEBHOOK_URL')
    workflow = os.environ.get('GITHUB_WORKFLOW')
    repo = os.environ.get('GITHUB_REPOSITORY')
    branch = os.environ.get('GITHUB_REF')
    commit = os.environ.get('GITHUB_SHA')

    commit_url = f'https://github.com/{repo}/commit/{commit}'
    repo_url = f'https://github.com/{repo}/tree/{branch}'

    color = action_color(job_status)
    status = action_status(job_status)
    emoji = action_emoji(job_status)

    message = f'{emoji} {workflow} {status} in <{repo_url}|{repo}@{branch}> on <{commit_url}|{commit[:7]}>.'

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

    requests.post(url, data=payload, headers=headers)


def main():
    job_status = os.environ["INPUT_STATUS"]
    notify_slack(job_status)


if __name__ == "__main__":
    main()
