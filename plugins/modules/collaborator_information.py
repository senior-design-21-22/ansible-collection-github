#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule
from github import Github
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


def add_collaborators(g, repos, to_add, org_name):
    for repo in repos:
        r = g.get_repo(org_name + "/" + repo)
        colab_list = []
        collaborators = r.get_collaborators(affiliation="direct")
        for collaborator in collaborators:
                colab_list.append(collaborator.login)
        for p in to_add:
            if (p not in colab_list):
                r.add_to_collaborators(p, permission=to_add[p])
                print("adding " + p + " to " + repo + " with Permission "  + to_add[p])

def check_permissions(g, repos, user, permission_level, org_name):
    status = False
    for repo in repos:
        r = g.get_repo(org_name + "/" + repo)
        status = (r.get_collaborator_permission(user) == permission_level)
    return status
        

def del_collaborators(g, repos, to_remove, org_name):
    for repo in repos:
        r = g.get_repo(org_name + "/" + repo)
        collaborators = r.get_collaborators(affiliation="direct")
        for collaborator in collaborators:
            if(collaborator.login in to_remove):
                r.remove_from_collaborators(collaborator.login)
                print("removing " + str(collaborator) + " from " + repo)

def del_collaborators(g, repos, to_remove, org_name):
    for repo in repos:
        r = g.get_repo(org_name + "/" + repo)
        collaborators = r.get_collaborators(affiliation="direct")
        for collaborator in collaborators:
            if(collaborator.login in to_remove):
                r.remove_from_collaborators(collaborator.login)
                print("removing " + str(collaborator) + " from " + repo)

def change_collaborator_permissions(g, repos, user, permssion_level, org_name):
    for repo in repos:
        r = g.get_repo(org_name + "/" + repo)
        colab_list = []
        collaborators = r.get_collaborators(affiliation="direct")
        for collaborator in collaborators:
            if (user == collaborator.login and permssion_level != r.get_collaborator_permission(user)):
                print("changing " + user + " in " + repo + " from Permission " + r.get_collaborator_permission(user) + " to "  + permssion_level)
                r.add_to_collaborators(user, permission=permssion_level)

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
            collab_output['permissions'] = collaborator.permissions

            dict_repo.append(collab_output.copy())

        output[repo] = dict_repo.copy()

    return output


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
    g = Github('token', base_url='https://github.ohio.edu/api/v3')
    org_name = "SSEP"

    repo_list = ["testing-repo-private", "testing-repo-internal", "testing-repo-public"]
    collaborators_to_remove = ["je652917"]
    target_repos = ["testing-repo-private"]
    collaborators_to_add = {"je652917":"admin"}
    perms_check = "je652917"

    if len(repo_list):
        for i in range(len(repo_list)):
            repo_list[i] = org_name + "/" + repo_list[i]
    
    output = get_collaborators(g, repo_list)

    print(output)
   
    #needed from ansible (list of dict [name, permission])
    # if(len(collaborators_to_add) > 0):
    #     if(len(target_repos) > 0):# needed from ansible (list)
    #         add_collaborators(g, target_repos, collaborators_to_add, org_name)

    # if(len(collaborators_to_remove) > 0):  # needed from ansible (list)
    #     if(len(target_repos) > 0):# needed from ansible (list)
    #         del_collaborators(g, target_repos, collaborators_to_remove, org_name)

    print(check_permissions(g, target_repos, perms_check, "admin", org_name))
    change_collaborator_permissions(g, target_repos, perms_check, "pull", org_name)
    
    print(get_collaborators(g, repo_list))

    # needed from ansible (list of dict [name, permission])
    if(len(collaborators_to_add) > 0):
        if(len(target_repos) > 0):# needed from ansible (list)
            add_collaberators(g, target_repos, collaborators_to_add)
        else:
            add_collaberators(g, repo_list, collaborators_to_add)

    if(len(collaborators_to_remove) > 0):  # needed from ansible (list)
        if(len(target_repos) > 0):# needed from ansible (list)
            del_collaberators(g, target_repos, collaborators_to_remove)
        else:
            del_collaberators(g, repo_list, collaborators_to_remove)
    
    print(get_collaborators(g, repo_list))


    if module.check_mode:
        return result

    module.exit_json(changed=True, msg=output)


def main():
    run_module()


if __name__ == '__main__':
    main()
