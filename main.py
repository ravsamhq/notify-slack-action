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


def construct_payload(inputs):
    """
    Creates a message payload which can be sent to Slack.
    """

    # derived from workflow environment
    workflow = os.getenv('GITHUB_WORKFLOW')
    repo = os.getenv('GITHUB_REPOSITORY')
    branch = os.getenv('GITHUB_REF')
    commit_sha = os.getenv('GITHUB_SHA')[:7]

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
    commit_url = f'https://github.com/{repo}/commit/{commit_sha}'
    repo_url = f'https://github.com/{repo}/tree/{branch}'
    color = action_color(job_status)
    status_message = action_status(job_status)
    emoji = action_emoji(job_status)

    # construct notification title
    title = title.replace('{emoji}', emoji)
    title = title.replace('{workflow}', workflow)
    title = title.replace('{status_message}', status_message)
    title = title.replace('{repo}', repo)
    title = title.replace('{repo_url}', repo_url)
    title = title.replace('{branch}', branch)
    title = title.replace('{commit_url}', commit_url)
    title = title.replace('{commit_sha}', commit_sha)

    # construct the message
    message = message.replace('{emoji}', emoji)
    message = message.replace('{workflow}', workflow)
    message = message.replace('{status_message}', status_message)
    message = message.replace('{repo}', repo)
    message = message.replace('{repo_url}', repo_url)
    message = message.replace('{branch}', branch)
    message = message.replace('{commit_url}', commit_url)
    message = message.replace('{commit_sha}', commit_sha)

    # added user mentions to the message
    if job_status in mention_users_when and mention_users.strip() != '':
        message += '\n'
        for user in mention_users.split(','):
            message = message + f'<@{user}> '

    # added group mentions to the message
    if job_status in mention_groups_when and mention_groups.strip() != '':
        message += '\n'
        for group in mention_groups.split(','):
            message = message + f'<!subteam^{group}> '

    # construct the footer
    footer = footer.replace('{emoji}', emoji)
    footer = footer.replace('{workflow}', workflow)
    footer = footer.replace('{status_message}', status_message)
    footer = footer.replace('{repo}', repo)
    footer = footer.replace('{repo_url}', repo_url)
    footer = footer.replace('{branch}', branch)
    footer = footer.replace('{commit_url}', commit_url)
    footer = footer.replace('{commit_sha}', commit_sha)

    payload = {
        'attachments': [
            {
                'text': message,
                'fallback': title,
                'pretext': title,
                'color': color,
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
