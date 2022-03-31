#!/usr/bin/python

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import absolute_import, division, print_function
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
    access_token:
        description:
            - GitHub API token used to manage a repository a user has access.
        required: true
        type: str
    api_url:
        description:
            - If using a token from a GitHub Enterprise account, the user must pass an enterprise URL.
              This URL must be structured as 'https://github.<ENTERPRISE DOMAIN>/api/v3/'.
        required: false
        type: str
    organization:
        description:
          - The organization containing the repository being managed.
        required: true
        type: str
    repository:
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
    team_name:
        description:
          - A team can be added through their name in the organization.
        required: false
        type: int
    auto_init:
        description:
          - This will initalize a README.md file when true
        required: false
        type: bool
    license_template:
        description:
          - License restrictions put on the repository. These can be found at
            'https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository'
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
    access_token: "12345"
    organization: SSEP
    api_url: https://github.<ENTERPRISE DOMAIN>/api/v3
    repository: brad-repo
    private: true
    description: "this is a test"
    homepage: "test homepage"
    has_issues: true
    has_wiki: false
    has_downloads: false
    has_projects: false
    team_name: tyler-team
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
    access_token: "12345"
    organization: SSEP
    api_url: https://github.<ENTERPRISE DOMAIN>/api/v3
    repository: brad-repo
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

import json
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.text.converters import jsonify
from github import Github
from numpy import outer
import requests


def run_module():
    module_args = dict(
        access_token=dict(type='str', required=True, no_log=True),
        organization=dict(type='str', required=True),
        api_url=dict(type='str', default=''),
        repository=dict(type='str', required=True),
        team_name=dict(type='str', default=0),
        visibility=dict(type='str', default='public'),
        has_issues=dict(type='bool', default=True),
        has_wiki=dict(type='bool', default=True),
        auto_init=dict(type='bool', default=False),
        has_downloads=dict(type='bool', default=False),
        has_projects=dict(type='bool', default=True),
        allow_squash_merge=dict(type='bool', default=True),
        allow_merge_commit=dict(type='bool', default=True),
        allow_rebase_merge=dict(type='bool', default=True),
        delete_branch_on_merge=dict(type='bool', default=False),
        description=dict(type='str', default=''),
        homepage=dict(type='str', default=''),
        license_template=dict(type='str', default=''),
        gitignore_template=dict(type='str', default=''),
        state=dict(type='str', default='present'),
    )

    valid_states = ["absent", "present"]
    valid_visibilities = ['public', 'private', 'internal']

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    initial = {}
    output_repo = {}

    if module.params['state'] not in valid_states:
        error_message = 'Invalid state: ' + module.params['state']
        module.exit_json(changed=False, err=error_message, failed=True)

    if module.params['visibility'] not in valid_visibilities:
        error_message = 'Invalid visibility: ' + module.params['visibility']
        module.exit_json(changed=False, err=error_message, failed=True)

    if module.params['api_url'] == '':
        g = Github(module.params['access_token'])
    else:
        g = Github(module.params['access_token'],
                   base_url=module.params['api_url'])

    getUrl = module.params['api_url'] + '/repos/' + \
        module.params['organization'] + \
        '/' + module.params['repository']

    initialReq = requests.get(
        getUrl, headers={'Content-type': 'application/json', 'Authorization': 'Bearer ' + module.params['access_token']})

    if initialReq.status_code == 404:  # repository does NOT exist
        if module.params['state'] == 'present':
            org = g.get_organization(module.params['organization'])
            for team in org.get_teams():
                if team.name == module.params['team_name']:
                    if module.check_mode:
                        if module.params['api_url']:
                            noApiurl = str(module.params['api_url']).replace(
                                "/api/v3", "")
                            clone_url = "%s/%s/%s.git" % (
                                noApiurl, module.params['organization'], module.params['repository'])
                            url = "%s/repos/%s/%s" % (
                                module.params['api_url'], module.params['organization'], module.params['repository'])
                            hooks_url = "%s/hooks" % (url)
                        else:
                            clone_url = "https://github.com/%s/%s.git" % (
                                module.params['organization'], module.params['repository'])
                            url = "https://github.com/api/v3/repos/%s/%s" % (
                                module.params['organization'], module.params['repository'])
                            hooks_url = "%s/hooks" % (url)
                        full_name = "%s/%s" % (
                            module.params['organization'], module.params['repository'])

                        output_repo = {
                            "allow_merge_commit": module.params['allow_merge_commit'],
                            "allow_rebase_merge": module.params['allow_rebase_merge'],
                            "allow_squash_merge": module.params['allow_squash_merge'],
                            "archived": False,
                            "clone_url": clone_url,
                            "default_branch": "main",
                            "delete_branch_on_merge": module.params['delete_branch_on_merge'],
                            "description": module.params['description'],
                            "full_name": full_name,
                            "has_downloads": module.params['has_downloads'],
                            "has_issues": module.params['has_issues'],
                            "has_projects": module.params['has_projects'],
                            "has_wiki": module.params['has_wiki'],
                            "homepage": module.params['homepage'],
                            "hooks_url": hooks_url,
                            "language": None,
                            "name": module.params['repository'],
                            "owner": module.params['organization'],
                            "visibility": module.params['visibility'],
                            "url": url
                        }
                    else:
                        url = module.params['api_url'] + '/orgs/' + \
                            module.params['organization'] + '/repos'

                        payload = {
                            "name": module.params['repository'],
                            "description": module.params['description'],
                            "homepage": module.params['homepage'],
                            "private": module.params['visibility'],
                            "has_issues": module.params['has_issues'],
                            "has_wiki": module.params['has_wiki'],
                            "has_downloads": module.params['has_downloads'],
                            "has_projects": module.params['has_projects'],
                            "team_id": team.id,
                            "visibility": module.params['visibility'],
                            "auto_init": module.params['auto_init'],
                            "license_template": module.params['license_template'],
                            "gitignore_template": module.params['gitignore_template'],
                            "allow_squash_merge": module.params['allow_squash_merge'],
                            "allow_merge_commit": module.params['allow_merge_commit'],
                            "allow_rebase_merge": module.params['allow_rebase_merge'],
                            "delete_branch_on_merge": module.params['delete_branch_on_merge']
                        }

                        requests.post(
                            url, json=payload, headers={'Content-type': 'application/json', 'Authorization': 'Bearer ' + module.params['access_token']})
    elif initialReq.status_code == 200:  # Repository DOES exist
        body = json.loads(initialReq.text)
        initial = {
            "name": body['name'],
            "full_name": body['full_name'],
            "owner": body['owner']['login'],
            "description": body['description'],
            "visibility": body['visibility'],
            "archived": body['archived'],
            "language": body['language'],
            "url": body['url'],
            "default_branch": body['default_branch'],
            "hooks_url": body['hooks_url'],
            "clone_url": body['clone_url'],
            "allow_merge_commit": body['allow_merge_commit'],
            "allow_rebase_merge": body['allow_rebase_merge'],
            "allow_squash_merge": body['allow_squash_merge'],
            "delete_branch_on_merge": body['delete_branch_on_merge'],
            "has_issues": body['has_issues'],
            "has_downloads": body['has_downloads'],
            "has_wiki": body['has_wiki'],
            "has_projects": body['has_projects'],
            "homepage": body['homepage']
        }

        if module.params['state'] == 'present':
            if module.check_mode:
                output_repo = initial.copy()
                output_repo['visibility'] = module.params["visibility"]
                output_repo['description'] = module.params["description"]
                output_repo['homepage'] = module.params["homepage"]
                output_repo['has_issues'] = module.params["has_issues"]
                output_repo['has_wiki'] = module.params["has_wiki"]
                output_repo['has_downloads'] = module.params["has_downloads"]
                output_repo['has_projects'] = module.params["has_projects"]
                output_repo['allow_merge_commit'] = module.params["allow_merge_commit"]
                output_repo['allow_rebase_merge'] = module.params["allow_rebase_merge"]
                output_repo['allow_squash_merge'] = module.params["allow_squash_merge"]
                output_repo['delete_branch_on_merge'] = module.params["delete_branch_on_merge"]
            else:
                org = g.get_organization(module.params['organization'])
                for team in org.get_teams():
                    if team.name == module.params['team_name']:
                        url = module.params['api_url'] + '/repos/' + \
                            module.params['organization'] + \
                            '/' + module.params['repository']
                        payload = {
                            "name": module.params['repository'],
                            "description": module.params['description'],
                            "homepage": module.params['homepage'],
                            "has_issues": module.params['has_issues'],
                            "has_wiki": module.params['has_wiki'],
                            "has_downloads": module.params['has_downloads'],
                            "has_projects": module.params['has_projects'],
                            "team_id": team.id,
                            "visibility": module.params['visibility'],
                            "auto_init": module.params['auto_init'],
                            "license_template": module.params['license_template'],
                            "gitignore_template": module.params['gitignore_template'],
                            "allow_squash_merge": module.params['allow_squash_merge'],
                            "allow_merge_commit": module.params['allow_merge_commit'],
                            "allow_rebase_merge": module.params['allow_rebase_merge'],
                            "delete_branch_on_merge": module.params['delete_branch_on_merge']
                        }
                        requests.patch(url, json=payload, headers={
                            'Content-type': 'application/json', 'Authorization': 'Bearer ' +
                                            module.params['access_token'], 'Accept': 'application/vnd.github.v3+json'})
        elif module.params['state'] == 'absent':
            if not module.check_mode:
                g.get_organization(module.params['organization']).get_repo(
                    module.params['repository']).delete()
            else:
                output_repo = {}

    finalReq = requests.get(
        getUrl, headers={'Content-type': 'application/json', 'Authorization': 'Bearer ' + module.params['access_token']})

    if finalReq.status_code == 404:
        output = {}
    else:
        body = json.loads(finalReq.text)

        output = {
            "name": body['name'],
            "full_name": body['full_name'],
            "owner": body['owner']['login'],
            "description": body['description'],
            "visibility": body['visibility'],
            "archived": body['archived'],
            "language": body['language'],
            "url": body['url'],
            "default_branch": body['default_branch'],
            "hooks_url": body['hooks_url'],
            "clone_url": body['clone_url'],
            "allow_merge_commit": body['allow_merge_commit'],
            "allow_rebase_merge": body['allow_rebase_merge'],
            "allow_squash_merge": body['allow_squash_merge'],
            "delete_branch_on_merge": body['delete_branch_on_merge'],
            "has_issues": body['has_issues'],
            "has_downloads": body['has_downloads'],
            "has_wiki": body['has_wiki'],
            "has_projects": body['has_projects'],
            "homepage": body['homepage']
        }
    if module.check_mode:
        module.exit_json(repo=output_repo, changed=initial != output_repo)
    else:
        module.exit_json(repo=output, changed=initial != output)


def main():
    run_module()


if __name__ == '__main__':
    main()
