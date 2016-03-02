
import json
import requests


def send_to_slack(body, webhook_url):
    requests.post(webhook_url, data=json.dumps(body))


def message_builder(pipeline, stage, status, changeset, changeset_url, dashboard_url):

    if status in ['passed', 'is fixed']:
        icon = ':white_check_mark:'
    elif status == 'failed':
        icon = ':x:'
    else:
        return

    if stage in ['Deploy', 'defaultStage', 'Default', 'DeployAll']:
        changeset_url = 'N/A'
        changeset = 'N/A'

    body = {'username': 'go build status - ' + status,
            'icon_emoji': icon,
            'text': '<' + (get_pipeline_url(dashboard_url, pipeline) + '|' + pipeline + '>'
                    '\n' + 'Stage: ' + stage +
                    '\n' + 'Changeset: <' + changeset_url + '|' + changeset + '>')}
    return body


def is_matching_send_rule(gocd_details):
    if gocd_details['status'] == 'failed':
        return True
    if gocd_details['status'] in ['passed', 'is fixed']:
        if gocd_details['stage'] in ['Package', 'Deploy',
                                     'Default', 'defaultStage',
                                     'DeployAll']:
            return True
    else:
        return False


def get_pipeline_url(gocd_dash_root_url, pipeline):
    return gocd_dash_root_url + '/tab/pipeline/history/' + pipeline
