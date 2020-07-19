def action_color(status):
    if status == 'success':
        return 'good'
    else if status == 'failure':
        return 'danger'
    else:
        return 'warning'


def action_status(status):
    if status == 'success':
        return 'passed'
    else if status == 'failure':
        return 'failed'
    else:
        return 'passed with warnings'


def action_emoji(status):
    if status == 'success':
        return ':sunglasses:'
    else if status == 'failure':
        return ':worried:'
    else:
        return ':zipper_mouth_face:'
