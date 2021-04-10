[![Create Release](https://github.com/ravsamhq/metafold-store-frontend/actions/workflows/release.yml/badge.svg)](https://github.com/ravsamhq/metafold-store-frontend/actions/workflows/release.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# Notify Slack Action

Send Github Actions workflow status notifications to Slack regarding failures, warnings or even success. You can read more about the action in [our blog post](https://www.ravsam.in/blog/send-slack-notification-when-github-actions-fails/).

## Minimal workflow

```yaml
steps:
  - uses: ravsamhq/notify-slack-action@master
    if: always()
    with:
      status: ${{ job.status }} # required
    env:
      SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }} # required
```

## Example workflow

The following variables are available for formatting your own strings.

- {branch}
- {commit_url}
- {commit_sha}
- {emoji}
- {repo}
- {repo_url}
- {status_message}
- {workflow}

You can use these to construct custom `notification_title`, `message_format` and `footer`. To get an idea see the workflow below.

```yaml
steps:
  - uses: ravsamhq/notify-slack-action@master
    if: always()
    with:
      status: ${{ job.status }} # required
      notification_title: '{workflow} has {status_message}' # optional
      message_format: '{emoji} *{workflow}* {status_message} in <{repo_url}|{repo}>' # optional
      footer: 'Linked Repo <{repo_url}|{repo}>' # optional
      notify_when: 'failure' # optional
    env:
      SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }} # required
```

## Tech Stack

- [Python](https://python.org/) - Programming
- [Slack Webhooks](https://slack.com/) - Notifications

## Development

Follow these instructions to get the project up and running.

```bash
# clone the repo
git clone https://github.com/ravsamhq/notify-slack-action.git

# change directory
cd notify-slack-action

# setup python virtual environment
python3 -m venv venv

# activate virtual environment
source venv/bin/activate

# install pip dependencies
pip install -r requirements.txt
```

## Versioning

This project uses [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/ravsamhq/notify-slack-action/tags).

## Contributors

- [Ravgeet Dhillon](https://github.com/ravgeetdhillon)

## Extra

- We are open for [issues and feature requests](https://github.com/ravsamhq/notify-slack-action/issues).
- In case you get stuck at somewhere, feel free to contact at [Mail](mailto:info@ravsam.in).

<small>&copy; 2021 RavSam Web Solutions</small>
