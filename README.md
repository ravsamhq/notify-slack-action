# Notify Slack Action

### Example workflow

```yaml
steps:
  - uses: ravsamhq/notify-slack-action@master
    if: always()
    with:
      status: ${{ job.status }}
    env:
      SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }} # required
      GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }} # optional
```

> Made in Python &bull; By [Ravgeet Dhillon](https://github.com/ravgeetdhillon) @ [RavSam](https://www.ravsam.in)
