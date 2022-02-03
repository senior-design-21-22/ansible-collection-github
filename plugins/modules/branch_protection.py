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


def get_branch_protections(g, repo, branch):
    output = {}
    try:
        branch = g.get_repo(repo).get_branch(branch)
        if not branch.protected:
            return output
        else:
            url = branch.protection_url
            output = {
                "url": branch.get_protection().url,
                "status_checks": json.dumps(branch.get_required_status_checks())
            }
            
            with open("/Users/bradleygolski/Desktop/ansibleOutput.txt", "w+") as temp:
                temp.write(str(output))
            return output
    
    except Exception as e:
        with open("/Users/bradleygolski/Desktop/ansibleOutput.txt", "w+") as temp:
            temp.write(str(e))
        return e

def run_module():
    module_args = dict(
        # action=dict(type='str', default='add'),
        token=dict(type='str', default='No Token Provided.'),
        organization_name=dict(
            type='str', default=''),
        enterprise_url=dict(type='str', default=''),
        repo=dict(type='str', default='No Repo Provided.'),
        branch=dict(type='str', default='No Branch Provided.'),
        # host=dict(type='str', default=''),
        # endpoint=dict(type='str', default=''),
        # events=dict(type='list', elements='str'),
        # content_type=dict(type='str', default=''),
        # change_events=dict(type='list', elements='str'),
        # active_status=dict(type='str', default=''),
        # add_events=dict(type='list', elements='str'),
        # remove_events=dict(type='list', elements='str'),
        # new_host=dict(type='str', default=''),
        # new_endpoint=dict(type='str', default=''),
        # new_content_type=dict(type='str', default='')
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    if(module.params['enterprise_url'] == ''):
        g = Github(module.params['token'])
    else:
        g = Github(module.params['token'],
                   base_url=module.params['enterprise_url'])

    if len(module.params['repo']):
        module.params['repo'] = module.params['organization_name'] + \
            "/" + module.params['repo']

    initial = get_branch_protections(g, module.params['repo'], module.params['branch'])
    if not initial:
        initial = []

    output = get_branch_protections(g, module.params['repo'], module.params['branch'])
    if not output:
        output = []
    result = dict(
        changed=initial != output,
        fact=''
    )

    if module.check_mode:
        return result

    module.exit_json(branch_protections=output, changed=initial != output)


def main():
    run_module()


if __name__ == '__main__':
    main()