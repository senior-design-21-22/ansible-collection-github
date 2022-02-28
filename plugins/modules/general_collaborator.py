#!/usr/bin/python

from __future__ import absolute_import, division, print_function
import collections
from email.policy import default
import json
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.text.converters import jsonify
from github import Github
from numpy import outer
__metaclass__ = type

ANSIBLE_METADATA = {
    'metadata_version': '1.0',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: general_repository

short_description: A module that manages a repository in an organization.

description:
  - "A module that creates, modifies, or deletes a repository in an organization."

options:
    token:
        description:
            - GitHub API token used to manage a repository a user has access.
        required: true
        type: str
    enterprise_url:
        description:
            - If using a token from a GitHub Enterprise account, the user must pass an enterprise URL.
              This URL must be structured as 'https://github.<ENTERPRISE DOMAIN>/api/v3/'.
        required: false
        type: str
    organization_name:
        description:
          - The organization containing the repository being managed.
        required: true
        type: str
    repo_name:
        description:
          - The name of the repository being managed.
        required: true
        type: str
    private:
        description:
          - The status of whether or not the repository will be private.
        required: false
        type: bool
    description:
        description:
          - Description of the repository. Will show up in the README.md and 'About'
        required: false
        type: str
    homepage:
        description:
          - Link or name of the homepage to the repository.
        required: false
        type: str
    has_issues:
        description:
          - Whether or not the repository will have the ability to create issues.
        required: false
        type: bool
    has_wiki:
        description:
          - Whether or not the repository will have a wiki tab.
        required: false
        type: bool
    has_downloads:
        description:
          - Whether or not the repository will have a downloads tab.
        required: false
        type: bool
    has_projects:
        description:
          - Whether or not the repository will have a projects tab.
        required: false
        type: bool
    team_id:
        description:
          - A team can be added through their ID number in the organization.
        required: false
        type: int
    auto_init:
        description:
          - This will initalize a README.md file when true
        required: false
        type: bool
    license_template:
        description:
          - License restrictions put on the repository. Example- 'gpl-3.0'
        required: false
        type: str
    gitignore_template:
        description:
          - Template for gitignore to use. These can be found at 'https://github.com/github/gitignore'
        required: false
        type: str
    allow_squash_merge:
        description:
          - Status of whether or not squash merges are allowable.
        required: false
        type: bool
    allow_merge_commit:
        description:
          - Status of whether or not merge commits are allowable.
        required: false
        type: bool
    allow_rebase_merge:
        description:
          - Status of whether or not rebase merges are allowable.
        required: false
        type: bool
    delete_branch_on_merge:
        description:
          - Status of whether or to delete the branch upon a merge.
        required: false
        type: bool
    state:
        description:
          - Whether 'present' or 'absent', this determines whether the creation/managing of a repo or the deletion of a repo is required.
        required: false
        type: bool

author:
    - Jacob Eicher (@jacobeicher)
    - Bradley Golski (@bgolski)
    - Tyler Zwolenik (@TylerZwolenik)
    - Nolan Khounborinn (@Khounborinn)
'''

EXAMPLES = '''
# Will create/manage repository
- name: "Create repository within enterprise organization"
  ohioit.github.general_repository:
    token: "12345"
    organization_name: SSEP
    enterprise_url: https://github.<ENTERPRISE DOMAIN>/api/v3
    repo_name: brad-repo
    private: true
    description: "this is a test"
    homepage: "test homepage"
    has_issues: true
    has_wiki: false
    has_downloads: false
    has_projects: false
    team_id: 46
    auto_init: true
    license_template: gpl-3.0
    gitignore_template: "Haskell"
    allow_squash_merge: true
    allow_merge_commit: false
    allow_rebase_merge: true
    delete_branch_on_merge: true
    state: present


- name: "Delete repository within enterprise organization"
  ohioit.github.general_repository:
    token: "12345"
    organization_name: SSEP
    enterprise_url: https://github.<ENTERPRISE DOMAIN>/api/v3
    repo_name: brad-repo
    state: absent
'''

RETURN = '''
repo:
    description: Dictionary of components of current repository
    type: dict
    returned: If Repo provided is valid within the organization

repo.allow_merge_commit:
    description: Status of whether or not merge commits are allowable.
    type: bool
    returned: If Repo provided is valid within the organization

repo.allow_rebase_merge:
    description: Status of whether or not rebase merges are allowable.
    type: bool
    returned: If Repo provided is valid within the organization

repo.allow_squash_merge:
    description: Status of whether or not squash merges are allowable.
    type: bool
    returned: If Repo provided is valid within the organization

repo.archived:
    description: The status of whether or not the repository is archived.
    type: bool
    returned: If Repo provided is valid within the organization

repo.clone_url:
    description: The URL in which one can locally clone a repository.
    type: str
    returned: If Repo provided is valid within the organization

repo.default_branch:
    description: Name of the branch that the repository will show on startup
    type: str
    returned: If Repo provided is valid within the organization

repo.delete_branch_on_merge:
    description: Status of whether or to delete the branch upon a merge.
    type: bool
    returned: If Repo provided is valid within the organization

repo.description:
    description: Description of the repository. Will show up in the README.md and 'About'
    type: str
    returned: If Repo provided is valid within the organization

repo.full_name:
    description: Full path to reach repository including the organization.
    type: str
    returned: If Repo provided is valid within the organization

repo.has_downloads:
    description: Whether or not the repository will have a downloads tab.
    type: bool
    returned: If Repo provided is valid within the organization

repo.has_issues:
    description: Whether or not the repository will have the ability to create issues.
    type: bool
    returned: If Repo provided is valid within the organization

repo.has_projects:
    description: Whether or not the repository will have a projects tab.
    type: bool
    returned: If Repo provided is valid within the organization

repo.has_wiki:
    description: Whether or not the repository will have a wiki tab.
    type: bool
    returned: If Repo provided is valid within the organization

repo.homepage:
    description: Link or name of the homepage to the repository.
    type: str
    returned: If Repo provided is valid within the organization

repo.hooks_url:
    description: The API URL of where to access the repository's hooks.
    type: str
    returned: If Repo provided is valid within the organization

repo.language:
    description: The primary language of the repository.
    type: str
    returned: If Repo provided is valid within the organization

repo.name:
    description: The name of the repository.
    type: str
    returned: If Repo provided is valid within the organization

repo.owner:
    description: The organization to which the repository belongs.
    type: str
    returned: If Repo provided is valid within the organization

repo.private:
    description: The status of whether or not the repository will be private.
    type: bool
    returned: If Repo provided is valid within the organization

repo.url:
    description: API URL of where the repository is accessible
    type: str
    returned: If Repo provided is valid within the organization
'''

def run_module():
    module_args = dict(
        access_token=dict(type='str', default='John Doe'),
        organization=dict(type='str', default='default'),
        api_url=dict(type='str', default=''),
        repository=dict(type='str', default=''),
        collaborator=dict(type='str', default=''),
        permission=dict(type='str', default=''),
        state=dict(type='str', default='present')
    )

    valid_states = ["absent", "present"]
    valid_permissions = ['push', 'pull', 'admin']

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    if module.params['state'] not in valid_states:
        error_message = 'Invalid state: ' + module.params['state']
        module.exit_json(changed=False, err=error_message, failed=True)

    if module.params['api_url'] == '':
        g = Github(module.params['access_token'])
    else:
        g = Github(module.params['access_token'],
                   base_url=module.params['api_url'])

    module.params['repository'] = module.params['organization'] + '/' + module.params['repository']
    initial = {}
    output = {}

    try: 
        github_collaborators = g.get_repo(module.params['repository']).get_collaborators(affiliation='direct')
        initial_collaborators = dict()
        current_collaborator = dict()
        for collaborator in github_collaborators:
            current_collaborator['login'] = collaborator.login
            current_collaborator['id'] = collaborator.id
            current_collaborator['type'] = collaborator.type
            current_collaborator['site_admin'] = collaborator.site_admin
            permissions = {
                'triage': collaborator.permissions.triage,
                'push': collaborator.permissions.push,
                'pull': collaborator.permissions.pull,
                'admin': collaborator.permissions.admin
            }
            current_collaborator['permissions'] = permissions
            initial_collaborators[module.params['repository']] = current_collaborator.copy()
            initial = initial_collaborators.copy()

    except Exception as e:
        initial = {}

    repository = g.get_repo(module.params['repository'])
    if module.params['state'] == 'present':
        
        if module.params['collaborator'] and module.params['permission'] not in valid_permissions:
            error_message = 'Invalid permissions: ' + module.params['permission']
            module.exit_json(changed=False, err=error_message, failed=True)

        repository.add_to_collaborators(module.params['collaborator'], permission=module.params['permission'])

    else:
        try:
            repository.remove_from_collaborators(module.params['collaborator'])

        except Exception as e:
            ...

    try:
        github_collaborators = g.get_repo(module.params['repository']).get_collaborators(affiliation='direct')
        output_collaborators = dict()
        current_collaborator = dict()
        for collaborator in github_collaborators:
            current_collaborator['login'] = collaborator.login
            current_collaborator['id'] = collaborator.id
            current_collaborator['type'] = collaborator.type
            current_collaborator['site_admin'] = collaborator.site_admin
            permissions = {
                'triage': collaborator.permissions.triage,
                'push': collaborator.permissions.push,
                'pull': collaborator.permissions.pull,
                'admin': collaborator.permissions.admin
            }
            current_collaborator['permissions'] = permissions
            output_collaborators[module.params['repository']] = current_collaborator.copy()
            output = output_collaborators.copy()
        
    except Exception as e:
        output = {}

    result = dict(
        changed=collections.Counter(initial) != collections.Counter(output)
    )

    if module.check_mode:
        return result

    module.exit_json(repo=output, changed=initial != output)


def main():
    run_module()


if __name__ == '__main__':
    main()
