#!/usr/bin/python

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {
    'metadata_version': '1.0',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: repository_information

short_description: A module that returns information about GitHub repositories

description:
  - "A module that fetches information about repositories that a GitHub user has access to inside an organization."

options:
    token:
        description:
            - GitHub API token used to retrieve information about repositories to which a user has access to
        required: true
        type: str
    enterprise_url:
        description:
            - If using a token from a GitHub Enterprise account, the user must pass an enterprise URL.
              This URL must be structured as 'https://github.<ENTERPRISE DOMAIN>/api/v3/repos/<ORGANIZATION NAME>/<REPO NAME>'.
        required: false
        type: str
    organization_name:
        description:
          - The organization in which the query will be run.
        required: true
        type: str

author:
    - Jacob Eicher (@jacobeicher)
    - Bradley Golski (@bgolski)
    - Tyler Zwolenik (@TylerZwolenik)
    - Nolan Khounborinn (@Khounborinn)
'''

EXAMPLES = '''
# Pass in an organization name and GitHub API token
- name: returns information about
  repository_webhooks:
    organization: "senior-design-21-22"
    github_token: "12345"


# Pass in an organization name, GitHub API token and enterprise URL
- name: returns information about
  repository_info:
    organization: "SSEP"
    github_token: "12345"
    enterprise_url: "https://github.<ENTERPRISE DOMAIN>/api/v3/repos/<ORGANIZATION NAME>/<REPO NAME>"
'''

RETURN = '''
webhooks:
    description: List contains dictionaries of webhooks and their information.
    type: list
    returned: if GitHub API token connects

repos.<ELEMENT INDEX>:
    description: Dictionary contains keys and values of a repository's information.
    type: dict
    returned: only if at least one repo is contained within organization

'''

from github import Github
from ansible.module_utils.common.text.converters import jsonify
from ansible.module_utils.basic import AnsibleModule
import json
import collections


def get_webhooks(g, repo_list):
    hooks = []
    current_hook_dict = {}
    for repo in repo_list:
        for current_hook in g.get_repo(repo).get_hooks():
            current_hook_dict = {}
            current_hook_dict = {
                "id": current_hook.id,
                "name": current_hook.name,
                "url": current_hook.url,
                "active": current_hook.active,
                "test_url": current_hook.test_url,
                "ping_url": current_hook.ping_url

            }
        hooks.append(current_hook_dict)
    output = [i for n, i in enumerate(hooks) if i not in hooks[n + 1:]]

    return output


def create_webhook(g, repo_list, org, events, host, endpoint):

    config = {
        "url": "http://%s/%s" % (host, endpoint),
        "content_type": "json"
    }

    for repo_name in repo_list:
        repo = g.get_repo(repo_name)
        repo.create_hook("web", config, events, active=True)


def run_module():
    changed = True
    module_args = dict(
        token=dict(type='str', default='No Token Provided.'),
        organization_name=dict(
            type='str', default=''),
        enterprise_url=dict(type='str', default=''),
        repos=dict(type='list', elements='str'),
        host=dict(type='str', default=''),
        endpoint=dict(type='str', default=''),
        events=dict(type='list', elements='str'),
        content_type=dict(type='str', default='')
    )

    valid_content_types = ["json", "form"]
    valid_events = ["branch_protection_rule",
                    "check_run",
                    "check_suite",
                    "code_scanning_alert",
                    "commit_comment",
                    "content_reference",
                    "create",
                    "delete",
                    "deploy_key",
                    "deployment",
                    "deployment_status",
                    "discussion",
                    "discussion_comment",
                    "fork",
                    "github_app_authorization",
                    "gollum",
                    "installation",
                    "installation_repositories",
                    "issue_comment",
                    "issues",
                    "label",
                    "marketplace_purchase",
                    "member",
                    "membership",
                    "meta",
                    "milestone",
                    "organization",
                    "org_block",
                    "package",
                    "page_build",
                    "ping",
                    "project_card",
                    "project_column",
                    "project",
                    "public",
                    "pull_request",
                    "pull_request_review",
                    "pull_request_review_comment",
                    "push",
                    "release",
                    "repository_dispatch",
                    "repository",
                    "repository_import",
                    "repository_vulnerability_alert",
                    "secret_scanning_alert",
                    "security_advisory",
                    "sponsorship",
                    "star",
                    "status",
                    "team",
                    "team_add",
                    "watch",
                    "workflow_dispatch",
                    "workflow_job"]

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    if(module.params['enterprise_url'] == ''):
        g = Github(module.params['token'])
    else:
        g = Github(module.params['token'],
                   base_url=module.params['enterprise_url'])

    if len(module.params['repos']):
        for i in range(len(module.params['repos'])):
            module.params['repos'][i] = module.params['organization_name'] + \
                "/" + module.params['repos'][i]

    initial = get_webhooks(g, module.params['repos'])

    if len(module.params['host']) and len(module.params['endpoint']):
        for event in module.params['events']:
            if event not in valid_events:
                module.exit_json(changed=False, err="Invalid event name")
        if module.params['content_type'] in valid_content_types:
            create_webhook(g, module.params['repos'], module.params['organization_name'],
                           module.params['events'], module.params['host'], module.params['endpoint'])

    output = get_webhooks(g, module.params['repos'])

    if initial == output:
        changed = False

    result = dict(
        changed=changed,
        fact=''
    )

    if module.check_mode:
        return result

    module.exit_json(webhooks=output)


def main():
    run_module()


if __name__ == '__main__':
    main()
