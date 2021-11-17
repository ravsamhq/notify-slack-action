"""
A Github Action to send Github Actions workflow status notifications to Slack.
Main module for the app.
"""

import json
import os
import requests
from dotenv import load_dotenv


def action_color(status):
    """
    Get a action color based on the workflow status.
    """

    if status == 'success':
        return 'good'
    elif status == 'failure':
        return 'danger'
    else:
        return 'warning'


def action_status(status):
    """
    Get a transformed status based on the workflow status.
    """

    if status == 'success':
        return 'passed'
    elif status == 'failure':
        return 'failed'
    else:
        return 'passed with warnings'


def action_emoji(status):
    """
    Get an emoji based on the workflow status.
    """

    if status == 'success':
        return ':heavy_check_mark:'
    elif status == 'failure':
        return ':x:'
    else:
        return ':large_orange_diamond:'


def get_workflow_url(inputs):
    """
    Get Workflow URL responsible for the Action run.
    """

    repo = os.getenv('GITHUB_REPOSITORY')
    token = inputs['token']

    url = f'https://api.github.com/repos/{repo}/actions/workflows'
    headers = {
        'Accept': 'application/vnd.github.v3+json',
        'Authorization': f'token {token}',
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        workflows = response.json()['workflows']
        for workflow in workflows:
            if workflow['name'] == os.getenv('GITHUB_WORKFLOW'):
                return workflow['html_url']

    return ''


def construct_payload(inputs):
    """
    Creates a message payload which can be sent to Slack.
    """

    # derived from workflow environment
    workflow = os.getenv('GITHUB_WORKFLOW')
    repo = os.getenv('GITHUB_REPOSITORY')
    branch = os.getenv('GITHUB_REF')
    commit_sha = os.getenv('GITHUB_SHA')[:7]
    run_id = os.getenv('GITHUB_RUN_ID')
    job_id = os.getenv('GITHUB_JOB')

    # derived from action inputs
    job_status = inputs['job_status']
    message = inputs['message_format']
    title = inputs['notification_title']
    footer = inputs['footer']
    mention_users = inputs['mention_users']
    mention_users_when = inputs['mention_users_when']
    mention_groups = inputs['mention_groups']
    mention_groups_when = inputs['mention_groups_when']

    # self constructed
    patterns = dict(
        repo=repo,
        branch=branch,
        commit_sha=commit_sha,
        commit_url=f'https://github.com/{repo}/commit/{commit_sha}',
        repo_url=f'https://github.com/{repo}',
        run_url=f'https://github.com/{repo}/actions/runs/{run_id}',
        job_url=f'https://github.com/{repo}/runs/{job_id}',
        workflow=workflow,
        workflow_url=get_workflow_url(inputs),
        color=action_color(job_status),
        status_message=action_status(job_status),
        emoji=action_emoji(job_status),
    )

    # construct notification title
    for k, v in patterns.items():
        title = title.replace('{%s}' % k, v)

    # construct the message
    for k, v in patterns.items():
        message = message.replace('{%s}' % k, v)

    # add user mentions to the message
    if job_status in mention_users_when and mention_users.strip() != '':
        message += '\n'
        for user in mention_users.split(','):
            message = message + f'<@{user}> '

    # add group mentions to the message
    if job_status in mention_groups_when and mention_groups.strip() != '':
        message += '\n'
        for group in mention_groups.split(','):
            message = message + f'<!subteam^{group}> '

    # construct the footer
    for k, v in patterns.items():
        footer = footer.replace('{%s}' % k, v)

    payload = {
        'attachments': [
            {
                'text': message,
                'fallback': title,
                'pretext': title,
                'color': patterns['color'],
                'mrkdwn_in': ['text'],
                'footer': footer,
            }
        ]
    }

    return json.dumps(payload)


def notify_slack(payload, testing=False):
    """
    Send a Slack notification.
    """

    if not testing:
        headers = {'Content-Type': 'application/json'}
        url = os.getenv('SLACK_WEBHOOK_URL')
        requests.post(url, data=payload, headers=headers)


def main(testing=False):
    """
    Main function for the app.
    """

    inputs = {
        'job_status': os.getenv('INPUT_STATUS'),
        'token': os.getenv('INPUT_TOKEN'),
        'notification_title': os.getenv('INPUT_NOTIFICATION_TITLE'),
        'message_format': os.getenv('INPUT_MESSAGE_FORMAT'),
        'footer': os.getenv('INPUT_FOOTER'),
        'notify_when': os.getenv('INPUT_NOTIFY_WHEN'),
        'mention_users': os.getenv('INPUT_MENTION_USERS'),
        'mention_users_when': os.getenv('INPUT_MENTION_USERS_WHEN'),
        'mention_groups': os.getenv('INPUT_MENTION_GROUPS'),
        'mention_groups_when': os.getenv('INPUT_MENTION_GROUPS_WHEN'),
    }

    payload = construct_payload(inputs)
    if inputs['job_status'] in inputs['notify_when'] and not testing:
        notify_slack(payload)


if __name__ == '__main__':
    load_dotenv()
    main()
