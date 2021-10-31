#!/usr/bin/python

from __future__ import absolute_import, division, print_function
from ansible.module_utils.basic import AnsibleModule
from github import Github
__metaclass__ = type

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
    - Tyler Zwolenik (@TylerZwolenik)
'''

EXAMPLES = '''
# Pass in an organization name and GitHub API token
- name: returns information about
  repository_info:
    organization: "senior-design-21-22"
    github_token: "12345"


# Pass in an organization name, GitHub API token
- name: returns information about
  repository_info:
    organization: "SSEP"
    github_token: "12345"
    enterprise_url: "<ENTERPRISE_URL>"
'''

RETURN = '''
repos:
    description: List contains dictionaries of repositories and their information.
    type: list
    returned: if GitHub API token connects
repos.<ELEMENT INDEX>:
    description: Dictionary contains keys and values of a repository's information.
    type: dict
    returned: only if at least one repo is contained within organization
repos.<ELEMENT INDEX>.name:
    description: Repository's name.
    type: str
    returned: only if organization contains a repository
repos.<ELEMENT INDEX>.full_name:
    description: Repository path name starting from organization.
    type: str
    returned: only if organization contains a repository
repos.<ELEMENT INDEX>.owner:
    description: Name of organization that owns the repository.
    type: str
    returned: only if organization contains a repository
repos.<ELEMENT INDEX>.description:
    description: Description of the repository. This field will be null unless previously set.
    type: str
    returned: only if organization contains a repository
repos.<ELEMENT INDEX>.private:
    description: Status whether the repository is private or public.
    type: bool
    returned: only if organization contains a repository
repos.<ELEMENT INDEX>.archived:
    description: Status of whether the repository is archived or not.
    type: bool
    returned: only if organization contains a repository
repos.<ELEMENT INDEX>.language:
    description: Repository language. This can be any language listed in 'https://github.com/github/linguist/blob/master/lib/linguist/languages.yml'.
    type: str
    returned: only if organization contains a repository
repos.<ELEMENT INDEX>.url:
    description: URL for repository. The provided URL is the route used for the GitHub API to be connected to Ansible.
                Non-enterprise URLs will be structured as 'https://api.github.com/repos/<ORGANIZATION NAME>/<REPO NAME>'.
                Enterprise URLs are structured as 'https://github.<ENTERPRISE DOMAIN>/api/v3/repos/<ORGANIZATION NAME>/<REPO NAME>'.
    type: str
    returned: only if organization contains a repository
repos.<ELEMENT INDEX>.default_branch:
    description: The branch that GitHub displays when anyone visits your repository.
    type: str
    returned: only if organization contains a repository
repos.<ELEMENT INDEX>.hooks_url:
    description: URL location where hooks are located within the repository when connected to the GitHub API.
                Non-enterprise URLs should be structured as 'https://api.github.com/repos/<ORGANIZATION NAME>/<REPO NAME>/hooks'.
                Enterprise URLs should be structured as 'https://github.<ENTERPRISE DOMAIN>/api/v3/repos/<ORGANIZATION NAME>/<REPO NAME>/hooks'.
    type: str
    returned: only if organization contains a repository
repos.<ELEMENT INDEX>.clone_url:
    description: URL location where repository will be accessible to be cloned.
                Non-enterprise URLs should be structured as 'https://github.com/<ORGANIZATION NAME>/<REPO NAME>.git'.
                Enterprise URLs should be structured as 'https://github.<ENTERPRISE DOMAIN>/<ORGANIZATION NAME>/<REPO NAME>.git'.
    type: str
    returned: only if organization contains a repository
repos.<ELEMENT INDEX>.visibility:
    description: The repository visibility status will be 'public', 'internal', or 'private'.
    type: str
    returned: only if organization contains a repository and is not a part of an enterprise account
repos.<ELEMENT INDEX>.is_template:
    description: The repository template status will true or false.
    type: bool
    returned: only if organization contains a repository and is not a part of an enterprise account
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
                print("adding " + p + " to " + repo +
                      " with Permission " + to_add[p])


def check_permissions(g, repos, user, permission_level, org_name):
    status = True
    for repo in repos:
        r = g.get_repo(org_name + "/" + repo)
        if(r.get_collaborator_permission(user) != permission_level):
            status = False
    return status


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
                print("changing " + user + " in " + repo + " from Permission " +
                      r.get_collaborator_permission(user) + " to " + permssion_level)
                r.add_to_collaborators(user, permission=permssion_level)


def get_collaborators(g, repo_list):

    output = dict()
    for repo in repo_list:
        dict_repo = list()
        collab_output = dict()
        collaborators = g.get_repo(
            repo).get_collaborators(affiliation="direct")
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
        token=dict(type='str', default='No Token Provided.'),
        organization_name=dict(
            type='str', default='No Organization Name Provided.'),
        enterprise_url=dict(type='str', default=''),
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
        g = Github(module.params['token'],
                   base_url=module.params['enterprise_url'])

    output = []

    # organization name retrieved from module's variables from playbook
    org_name = module.params['organization_name']

    for repo in g.get_organization(org_name).get_repos():
        if len(module.params["enterprise_url"]) == 0:
            current_repo_dict = {
                "owner": repo.owner.login,
                "description": repo.description,
                "private": repo.private,
                "archived": repo.archived,
                "language": repo.language,
                "url": repo.url,
                "default_branch": repo.default_branch,
                "hooks_url": repo.hooks_url,
                "clone_url": repo.clone_url,
                "visibility": repo.raw_data["visibility"],
                "is_template": repo.raw_data["is_template"]
            }
        else:
            current_repo_dict = {
                "owner": repo.owner.login,
                "description": repo.description,
                "private": repo.private,
                "archived": repo.archived,
                "language": repo.language,
                "url": repo.url,
                "default_branch": repo.default_branch,
                "hooks_url": repo.hooks_url,
                "clone_url": repo.clone_url
            }
        output.append(current_repo_dict)
    if module.check_mode:
        return result

    module.exit_json(repos=output)  # PUTS RESULT INTO result.repos


def main():
    run_module()


if __name__ == '__main__':
    main()
