#!/usr/bin/python


import json
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.text.converters import jsonify
from github import Github
ANSIBLE_METADATA = {
    'metadata_version': '1.0',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---

module: collaborator_information
short_description: A module that manages collaborators on repositories

  - "A module that fetches information about collaborators in repositories that a GitHub user has access to inside an organization."
options:
    token:
        description:
            - GitHub API token used to retrieve information about collaborators in repositories a user has access to
        required: true
        type: str

    enterprise_url:
        description:
            - If using a token from a GitHub Enterprise account, the user must pass an enterprise URL
        required: false
        type: str

    organization_name:
        description:
          - The organization that the information is within the scope of.
        required: true
        type: str
    repos:
        description:
          - The list of repositories that will be managed.
        required: true
        type: str
    collaborators_to_add:
        description:
          - The list of collaborators that will be added to the list of repos.
        required: false
        type: str
    collaborators_to_remove:
        description:
          - The list of collaborators that will be removed to the list of repos.
        required: false
        type: str
    check_collaborator:
        description:
          - The list of collaborators to check their permissions
         required: false
         type: str
    collaborators_to_change:
        description:
          - The list of collaborators to change permissions
         required: false
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
    {
        repo ("repo name"):
        [
            {
                "login":                owner name as string,

                "id":                   description as int,

                "type":                 user type as string

                "site_admin":           site admin access as boolean,

                "permissions":          user permissions as Permissions dictionary
            },
            {
                ...
            }
        ]
    },
    {
        ...
    }
'''


def add_collaborators(g, repos, to_add):         
    for repo in repos:
        r = g.get_repo(repo)
        collaborator_list = []
        collaborators = r.get_collaborators(affiliation="direct")
        for collaborator in collaborators:
                collaborator_list.append(collaborator.login)
        for p in to_add:
            if (p not in collaborator_list):
                r.add_to_collaborators(p, permission=to_add[p])

def check_permissions(g, repos, user_to_check):
    status = True
    for repo in repos:
        r = g.get_repo(repo)
        for user in user_to_check.items():
            if(r.get_collaborator_permission(user[0]) != user[1]):
                status = False
    return status
        

def del_collaborators(g, repos, to_remove):
    for repo in repos:
        r = g.get_repo(repo)
        collaborators = r.get_collaborators(affiliation="direct")
        for collaborator in collaborators:
            if(collaborator.login in to_remove):
                r.remove_from_collaborators(collaborator.login)


def change_collaborator_permissions(g, repos, to_change):
    for repo in repos:
        r = g.get_repo(repo)
        collaborator_list = []
        collaborators = r.get_collaborators(affiliation="direct")
        for collaborator in collaborators:
                collaborator_list.append(collaborator.login)
        for p in to_change:
            if (p in collaborator_list):
                r.add_to_collaborators(p, permission=to_change[p])


def get_collaborators(g, repo_list):

    output = dict()
    for repo in repo_list:
        dict_repo = list()
        collab_output = dict()
        collaborators = g.get_repo(repo).get_collaborators(affiliation="direct")
        for collaborator in collaborators:
             
            collab_output['login'] = collaborator.login
            collab_output['id'] = collaborator.id
            # collab_output['node_id'] = collaborator.node_id
            # collab_output['avatar_url'] = collaborator.avatar_url
            # collab_output['gravatar_id'] = collaborator.gravatar_id
            # collab_output['url'] = collaborator.url
            # collab_output['html_url'] = collaborator.html_url
            # collab_output['followers_url'] = collaborator.followers_url
            # collab_output['following_url'] = collaborator.following_url
            # collab_output['gists_url'] = collaborator.gists_url
            # collab_output['starred_url'] = collaborator.starred_url
            # collab_output['subscriptions_url'] = collaborator.subscriptions_url
            # collab_output['organizations_url'] = collaborator.organizations_url
            # collab_output['repos_url'] = collaborator.repos_url
            # collab_output['events_url'] = collaborator.events_url
            # collab_output['received_events_url'] = collaborator.received_events_url
            collab_output['type'] = collaborator.type
            collab_output['site_admin'] = collaborator.site_admin
            permissions = json.dumps({
                'triage': collaborator.permissions.triage,
                'push': collaborator.permissions.push,
                'pull': collaborator.permissions.pull,
                'admin': collaborator.permissions.admin
                })
            collab_output['permissions'] = permissions


            dict_repo.append(collab_output.copy())

        output[repo] = dict_repo.copy()

    return output


def run_module():
    module_args = dict(
        token=dict(type='str', default='John Doe'),
        organization_name=dict(type='str', default='default'),
        enterprise_url=dict(type='str', default=''),
        repos=dict(type='list', elements='str'),
        collaborators_to_add=dict(type='dict'),
        check_collaborator=dict(type='dict'),
        collaborators_to_change=dict(type='dict'),
        collaborators_to_remove=dict(type='list', elements='str'),

    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    result = dict(
        changed=False,
        fact=''
    )

    # token usage retrieved from module's variables from playbook
    if(module.params['enterprise_url'] == ''):
        g = Github(module.params['token'])
    else:
        g = Github(module.params['token'], base_url=module.params['enterprise_url'])


    if len(module.params['repos']):
        for i in range(len(module.params['repos'])):
            module.params['repos'][i] = module.params['organization_name'] + "/" + module.params['repos'][i]

    if(module.params['collaborators_to_add']):
        if len(module.params['collaborators_to_add']) and len(module.params['repos']):
            add_collaborators(g, module.params['repos'], module.params['collaborators_to_add'])

    if(module.params['collaborators_to_remove'] and len(module.params['repos'])):
        del_collaborators(g, module.params['repos'], module.params['collaborators_to_remove'])
    
    if(module.params['check_collaborator'] and len(module.params['repos'])):
        check_permissions(g, module.params['repos'], module.params['check_collaborator'])

    if(module.params['collaborators_to_change'] and len(module.params['repos'])):
        check_permissions(g, module.params['repos'], module.params['collaborators_to_change'])


    output = get_collaborators(g,  module.params['repos'])


    if module.check_mode:
        return result

    module.exit_json(changed=True, msg=output)


def main():
    run_module()


if __name__ == '__main__':
    main()
