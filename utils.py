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
