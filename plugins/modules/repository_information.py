#!/usr/bin/python
from github import Github
from ansible.module_utils.basic import AnsibleModule

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
    - Tyler Zwolenik (@TylerZwolenik)
'''

EXAMPLES = '''
# Pass in an organization name and github API token
- name: returns information about 
  repository_info:
    organization: "ohioit"
    github_token: "12345"
'''

RETURN = '''
repo ("repo name"):

    "owner":            owner name as string,

    "description":      description as string,

    "private":          repo status (bool: true or false),

    "is_template":      if it is template (bool: true or false),

    "archived":         archived status of repository (bool: true or false),

    "language":         language that the repo is using (as string),

    "visibility":       for other users ("private" or "public"),

    "url":              url for repo (as string),

    "default_branch":   branch that repo defaults to (as string),

    "hooks_url":        url for hooks (as string),

    "clone_url":        url for cloning (as string)
'''



def run_module():
    module_args = dict(
        token=dict(type='str', default='No Token Provided.'),
        organization_name=dict(type='str', default='No Organization Name Provided.'),
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
    ghub = Github(module.params['token'])

    output = {"repos": {}}

    #organization name retrieved from module's variables from playbook
    org_name = module.params['organization_name']

    for repo in ghub.get_organization(org_name).get_repos():
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
            "clone_url": repo.clone_url,
            }

    if module.check_mode:
        return result

    module.exit_json(**output)

def main():
    run_module()

if __name__ == '__main__':
    main()
