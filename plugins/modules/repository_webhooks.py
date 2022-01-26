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


def get_webhooks(g, repo):
    hooks = []
    current_hook_dict = {}
    for current_hook in g.get_repo(repo).get_hooks():
        current_hook_dict = {}
        current_hook_dict = {
            "id": current_hook.id,
            "config": current_hook.config,
            "name": current_hook.name,
            "url": current_hook.url,
            "active": current_hook.active,
            "test_url": current_hook.test_url,
            "ping_url": current_hook.ping_url,
            "events": current_hook.events
        }
        hooks.append(current_hook_dict)
    output = [i for n, i in enumerate(hooks) if i not in hooks[n + 1:]]

    return output


def create_webhook(g, repo, events, host, endpoint, content_type):
    
    config = {
        "url": "http://%s/%s" % (host, endpoint),
        "content_type": content_type
    }

    for current_hook in g.get_repo(repo).get_hooks():
        if collections.Counter(current_hook.events) == collections.Counter(events) and config["url"] == current_hook.config["url"] and current_hook.config["content_type"] == content_type:
                return

    repo = g.get_repo(repo)
    repo.create_hook("web", config, events, active=True)
    
def delete_webhook(g, repo, events, host, endpoint, content_type):
    url = "http://" + host + "/" + endpoint

    for current_hook in g.get_repo(repo).get_hooks():
        if collections.Counter(current_hook.events) == collections.Counter(events) and url == current_hook.config["url"] and current_hook.config["content_type"] == content_type:
                current_hook.delete()
                
def edit_webhook(g, repo, events, host, endpoint, content_type, active_status, add_events, remove_events, new_host, new_endpoint, new_content_type):
    url = "http://" + host + "/" + endpoint
    if new_host:
        host=new_host
    if new_endpoint:
        endpoint=new_endpoint
    config = {
        "url": "http://%s/%s" % (host, endpoint),
        "content_type": content_type
    }
    for current_hook in g.get_repo(repo).get_hooks():
        if collections.Counter(current_hook.events) == collections.Counter(events) and url == current_hook.config["url"] and current_hook.config["content_type"] == content_type:
            if new_host:
                host=new_host
            if new_endpoint:
                endpoint=new_endpoint
            if new_content_type:
                content_type=new_content_type
            new_config = {
                "url": "http://%s/%s" % (host, endpoint),
                "content_type": content_type
            }
            if new_host or new_endpoint or new_content_type:
                current_hook.edit("web", new_config)
            if active_status.lower()=="false":
                current_hook.edit("web", new_config, active=False)
            if active_status.lower()=="true":
                current_hook.edit("web", new_config, active=True)
            if add_events:
                current_hook.edit("web", new_config, add_events=add_events)
            if remove_events:
                current_hook.edit("web", new_config, remove_events=remove_events)

def run_module():
    module_args = dict(
        action=dict(type='str', default='add'),
        token=dict(type='str', default='No Token Provided.'),
        organization_name=dict(
            type='str', default=''),
        enterprise_url=dict(type='str', default=''),
        repo=dict(type='str', default='No Repo Provided.'),
        host=dict(type='str', default=''),
        endpoint=dict(type='str', default=''),
        events=dict(type='list', elements='str'),
        content_type=dict(type='str', default=''),
        change_events=dict(type='list', elements='str'),
        active_status=dict(type='str', default=''),
        add_events=dict(type='list', elements='str'),
        remove_events=dict(type='list', elements='str'),
        new_host=dict(type='str', default=''),
        new_endpoint=dict(type='str', default=''),
        new_content_type=dict(type='str', default='')
    )

    valid_content_types = ["json", "form"]
    valid_actions = ["add", "delete", "edit"]
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

    if module.params['action'] not in valid_actions:
        error_message = 'Invalid action: ' + module.params['action']
        module.exit_json(changed=False, err=error_message, failed=True)

    if(module.params['enterprise_url'] == ''):
        g = Github(module.params['token'])
    else:
        g = Github(module.params['token'],
                   base_url=module.params['enterprise_url'])

    if len(module.params['repo']):
        module.params['repo'] = module.params['organization_name'] + \
            "/" + module.params['repo']

    initial = get_webhooks(g, module.params['repo'])

    if len(module.params['host']) and len(module.params['endpoint']):
        for event in module.params['events']:
            if event not in valid_events:
                error_message = 'Invalid event name: ' + event
                module.exit_json(changed=False, err=error_message, failed=True)
        if module.params['add_events']:
            for event in module.params['add_events']:
                if event not in valid_events:
                    error_message = 'Invalid event name: ' + event
                    module.exit_json(changed=False, err=error_message, failed=True)
        if module.params['remove_events']:                 
            for event in module.params['remove_events']:
                if event not in valid_events:
                    error_message = 'Invalid event name: ' + event
                    module.exit_json(changed=False, err=error_message, failed=True)                  
                
        if module.params['action'].lower() == 'add':
            if module.params['content_type'] in valid_content_types:
                create_webhook(g, module.params['repo'],
                            module.params['events'], module.params['host'], module.params['endpoint'], module.params['content_type'])
        elif module.params['action'].lower() == 'delete':
            delete_webhook(g, module.params['repo'],
                        module.params['events'], module.params['host'], module.params['endpoint'], module.params['content_type'])
        elif module.params['action'].lower() == 'edit':
            edit_webhook(g, module.params['repo'],
                        module.params['events'], module.params['host'], module.params['endpoint'], module.params['content_type'],
                        module.params['active_status'], module.params['add_events'], module.params['remove_events'], 
                        module.params['new_host'], module.params['new_endpoint'], module.params['new_content_type'])
    output = get_webhooks(g, module.params['repo'])

    result = dict(
        changed=initial != output,
        fact=''
    )

    if module.check_mode:
        return result

    module.exit_json(webhooks=output, changed=initial != output)


def main():
    run_module()


if __name__ == '__main__':
    main()
