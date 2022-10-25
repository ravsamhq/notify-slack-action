[![Create Release](https://github.com/ravsamhq/notify-slack-action/actions/workflows/release.yml/badge.svg)](https://github.com/ravsamhq/notify-slack-action/actions/workflows/release.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# Notify Slack Action

Send Github Actions workflow status notifications to Slack regarding failures, warnings or even success. You can read more about the action in [our blog post](https://www.ravsam.in/blog/send-slack-notification-when-github-actions-fails/).

## Features

- [x] Ability to control when to send notification
- [x] Custom Notification Title, Message and Footer using template variables
- [x] Mention Users and control when to mention them
- [x] Mention Users Groups and control when to mention them
- [x] Customize icons based on the action status

## Example workflows

### Minimal workflow

![](screenshots/minimal.png)

```yaml
steps:
  - uses: ravsamhq/notify-slack-action@v2
    if: always()
    with:
      status: ${{ job.status }} # required
    env:
      SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }} # required
```

### Extended Example without User Mentions

![](screenshots/without-mentions.png)

```yaml
steps:
  - uses: ravsamhq/notify-slack-action@v2
    if: always()
    with:
      status: ${{ job.status }}
      token: ${{ secrets.GITHUB_TOKEN }}
      notification_title: "{workflow} has {status_message}"
      message_format: "{emoji} *{workflow}* {status_message} in <{repo_url}|{repo}>"
      footer: "Linked Repo <{repo_url}|{repo}> | <{workflow_url}|View Workflow>"
      notify_when: "failure"
    env:
      SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
```

### Extended Example with User Mentions

![](screenshots/with-mentions.png)

```yaml
steps:
  - uses: ravsamhq/notify-slack-action@v2
    if: always()
    with:
      status: ${{ job.status }}
      notification_title: "{workflow} has {status_message}"
      message_format: "{emoji} *{workflow}* {status_message} in <{repo_url}|{repo}>"
      footer: "Linked Repo <{repo_url}|{repo}>"
      notify_when: "failure"
      mention_users: "U0160UUNH8S,U0080UUAA9N"
      mention_users_when: "failure,warnings"
    env:
      SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
```

> To get the Slack Member IDs, open the User profile you want to mention. Click _More_ and _Copy Member ID_.

### Extended Example with Users Groups Mentions

```yaml
steps:
  - uses: ravsamhq/notify-slack-action@v2
    if: always()
    with:
      status: ${{ job.status }}
      notification_title: "{workflow} has {status_message}"
      message_format: "{emoji} *{workflow}* {status_message} in <{repo_url}|{repo}>"
      footer: "Linked Repo <{repo_url}|{repo}>"
      notify_when: "failure"
      mention_users: "U0160UUNH8S,U0080UUAA9N"
      mention_users_when: "failure,warnings"
      mention_groups: "SAZ94GDB8"
      mention_groups_when: "failure,warnings"
    env:
      SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
```

To mention a channel, you can configure the `mention_groups` key like:

```yaml
mention_groups: "SAZ94GDB8,!channel"
```

The following variables are available for formatting your own strings.

- {branch}
- {branch_url}
- {commit_url}
- {commit_sha}
- {emoji}
- {repo}
- {repo_url}
- {status_message}
- {run_url}
- {job}
- {workflow}
- {workflow_url}

You can use these to construct custom `notification_title`, `message_format` and `footer`.

> In order to use `{workflow_url}`, specify the `token` input as `token: ${{ secrets.GITHUB_TOKEN }}`.

The above mentioned strings are available by default. However, you can use the following method to use any kind of data available in GitHub Actions:

1. Add the following step to get all the information related to your GitHub context

```yml
steps:
  - run: echo "${{ toJson(github) }}"
```

2. Then you can reference the `github` object properties:

```
github.event.head_commit.author.name
github.event.head_commit.message
```

as

```yml
steps:
  - uses: ravsamhq/notify-slack-action@v2
    if: always()
    with:
      ...
      message_format: '{emoji} ${{ github.event.head_commit.author.name }} ${{ github.event.head_commit.message }}'
    env:
      SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
```

## Inputs

```yml
status:
  description: Job Status
  required: true

token:
  description: Github Token for accessing workflow url
  required: false
  default: ""

notification_title:
  description: Specify on the notification message title
  required: false
  default: "New Github Action Run"

message_format:
  description: Specify on the notification message format
  required: false
  default: "{emoji} *{workflow}* {status_message} in <{repo_url}|{repo}@{branch}> on <{commit_url}|{commit_sha}>"

footer:
  description: Specify the footer of the message
  required: false
  default: "<{run_url}|View Run> | Developed by <https://www.ravsam.in|RavSam>"

notify_when:
  description: Specify on which events a slack notification is sent
  required: false
  default: "success,failure,cancelled,warnings,skipped"

mention_users:
  description: Specify the slack IDs of users you want to mention.
  required: false
  default: ""

mention_users_when:
  description: Specify on which events you want to mention the users
  required: false
  default: "success,failure,cancelled,warnings,skipped"

mention_groups:
  description: Specify the slack IDs of groups you want to mention
  required: false
  default: ""

mention_groups_when:
  description: Specify on which events you want to mention the groups
  required: false
  default: "success,failure,cancelled,warnings,skipped"

icon_success:
  description: Specify on icon to be used when event is success
  required: false
  default: ":heavy_check_mark:"

icon_failure:
  description: Specify on icon to be used when event is failure
  required: false
  default: ":x:"

icon_cancelled:
  description: Specify on icon to be used when event is cancelled
  required: false
  default: ":x:"

icon_warnings:
  description: Specify on icon to be used when event is warnings
  required: false
  default: ":large_orange_diamond:"

icon_skipped:
  description: Specify on icon to be used when event is skipped
  required: false
  default: ":fast_forward:"
```

## Development

Follow these instructions to get the project up and running:

```bash
# clone the repo
git clone https://github.com/ravsamhq/notify-slack-action.git

# change directory
cd notify-slack-action

# install dependencies
npm install
```

## Versioning

This project uses [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/ravsamhq/notify-slack-action/tags).

## Authors

- [Ravgeet Dhillon](https://github.com/ravgeetdhillon)

## Contributors

- [Ravgeet Dhillon](https://github.com/ravgeetdhillon)
- [Jirka Borovec](https://github.com/Borda)
- [Vlad Pronsky](https://github.com/vladkens)
- [erezarnon](https://github.com/erezarnon)

> Special shoutout to [Vlad Pronsky](https://github.com/vladkens) for porting the original Python based code to Typescript.

## Extra

- We are open for [issues and feature requests](https://github.com/ravsamhq/notify-slack-action/issues).
- In case you get stuck at somewhere, feel free to contact at our [Mail](mailto:info@ravsam.in).

<small>&copy; 2022 RavSam Web Solutions</small>
