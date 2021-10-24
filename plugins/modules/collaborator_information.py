#!/usr/bin/python

ANSIBLE_METADATA = {
    'metadata_version': '1.0',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: repository_info
short_description: A module that returns information about GitHub collaborators in organization repositories
description:
  - "A module that fetches information about collaborators in repositories that a GitHub user has access to inside an organization."
options:
    token:
        description:
            - GitHub API token used to retrieve information about collaborators in repositories a user has access to
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
    - Nolan Khounborin (@Khounborinn)
'''

EXAMPLES = '''
# Pass in an github API token and organization name
- name: returns information about 
  repository_info:
    github_token: "12345"
    organization: "ohioit"
'''

RETURN = '''
repo ("repo name"):

    "login":                owner name as string,

    "id":                   description as string,

    "node_id":              repo status (bool: true or false),

    "avatar_url":           if it is template (bool: true or false),

    "gravatar_id":          archived status of repository (bool: true or false),

    "url":                  language that the repo is using (as string),

    "html_url":             for other users ("private" or "public"),

    "followers_url":        url for repo (as string),

    "following_url":        branch that repo defaults to (as string),

    "gists_url":            url for hooks (as string),

    "starred_url":          url for cloning (as string)

    "subscriptions_url":    branch that repo defaults to (as string),

    "organizations_url":    url for hooks (as string),

    "repos_url":            url for cloning (as string)

    "events_url":           branch that repo defaults to (as string),

    "received_events_url":  url for hooks (as string),

    "type":                 url for cloning (as string)

    "site_admins":          branch that repo defaults to (as string),

    "permissions":          url for hooks (as string),
'''

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
    org_name = module.params['organization_name']

    for repo in g.get_organization(org_name).get_repos():
        repo_list.append(repo.full_name)

    output = list()
    for repo in repo_list:
        dict_repo = dict()
        dict_output = dict()
        collaborators = g.get_repo(repo).get_collaborators()
        for collaborator in collaborators:
            dict_output['login'] = collaborator.login
            dict_output['id'] = collaborator.id
            dict_output['node_id'] = collaborator.node_id
            dict_output['avatar_url'] = collaborator.avatar_url
            dict_output['gravatar_id'] = collaborator.gravatar_id
            dict_output['url'] = collaborator.url
            dict_output['html_url'] = collaborator.html_url
            dict_output['followers_url'] = collaborator.followers_url
            dict_output['following_url'] = collaborator.following_url
            dict_output['gists_url'] = collaborator.gists_url
            dict_output['starred_url'] = collaborator.starred_url
            dict_output['subscriptions_url'] = collaborator.subscriptions_url
            dict_output['organizations_url'] = collaborator.organizations_url
            dict_output['repos_url'] = collaborator.repos_url
            dict_output['events_url'] = collaborator.events_url
            dict_output['received_events_url'] = collaborator.received_events_url
            dict_output['type'] = collaborator.type
            dict_output['site_admin'] = collaborator.site_admin
            dict_output['permissions'] = collaborator.permissions

        dict_repo[repo] = dict_output
        output.append(dict_repo)

    if module.check_mode:
        return result

    module.exit_json(changed=True, msg=output)


def main():
    run_module()


if __name__ == '__main__':
    main()
