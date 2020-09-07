![Test](https://github.com/ravsamhq/notify-slack-action/workflows/Test/badge.svg)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# Notify Slack Action

Send workflow status notifications to Slack.

### Example workflow

```yaml
steps:
  - uses: ravsamhq/notify-slack-action@master
    if: always()
    with:
      status: ${{ job.status }}
      notify_when: 'failure' # default: 'success,failure,warnings'
    env:
      SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }} # required
      GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }} # optional
```

> Made in Python &bull; By [Ravgeet Dhillon](https://github.com/ravgeetdhillon) @ [RavSam Web Solutions](https://www.ravsam.in).
