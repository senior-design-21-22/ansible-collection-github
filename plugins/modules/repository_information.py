#!/usr/bin/python

ANSIBLE_METADATA = {
    'metadata_version': '1.0',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: repository_info
short_description: A module that returns information about GitHub repositories
description:
  - "A module that fetches information about repositories that a GitHub user has access to inside an organization."
options:
    token:
        description:
            - GitHub API token used to retrieve information about repositories a user has access to
        required: true
        type: str
    organization_name:
        description:
          - The organization that the information is within the scope of.
        required: true
        type: str
author:
    - Jacob Eicher (@jacobeicher)
    - Bradley Golski (@bgolski)
'''

# EXAMPLES = '''
# # Pass in an organization name and github API token
# - name: returns information about 
#   repository_info:
#     organization: "ohioit"
#     github_token: "12345"
# '''

# RETURN = '''
# fact:
#   description: 
#   type: 
#   sample: 
# '''

import json
from github import Github
from ansible.module_utils.basic import AnsibleModule

def run_module():
    module_args = dict(
        token=dict(type='str', default='John Doe'),
        organization_name=dict(type='str', default='default'),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    result = dict(
        changed=False,
        fact=''
    )
    #token usage retrieved from module's variables from playbook
    g = Github(module.params['token'])

    output = {"repos": {}}
    org_name = module.params['organization_name']
    for repo in g.get_organization(org_name).get_repos():
        output["repos"][repo.name] = {
            "owner": repo.owner.login,
            "description": repo.description,
            "private": repo.private,
            "is_template": repo.raw_data["is_template"],
            "archived": repo.archived,
            "language": repo.language,
            "visibility": repo.raw_data["visibility"],
            "url": repo.url,
            "default_branch": repo.default_branch,
            "hooks_url": repo.hooks_url,
            "clone_url": repo.clone_url
            }
    if module.check_mode:
        return result

    module.exit_json(**output)


def main():
    run_module()


if __name__ == '__main__':
    main()
