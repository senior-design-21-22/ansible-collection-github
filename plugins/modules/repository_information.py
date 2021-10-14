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
import random
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

    result['fact'] = module.params['token']

    if module.check_mode:
        return result

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
