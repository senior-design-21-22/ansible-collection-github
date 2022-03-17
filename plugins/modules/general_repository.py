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


# def check_repo_name(g, organization, repo):
#     org = g.get_organization("org-name")


def run_module():
    module_args = dict(
        access_token=dict(type='str', default='No Token Provided.'),
        organization=dict(type='str', default=''),
        api_url=dict(type='str', default=''),
        repository_name=dict(type='str', default=''),
        team_name=dict(type='str', default=0),
        private=dict(type='bool', default=False),
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

    valid_gitignore_templates = ['Actionscript',
                                 'Ada',
                                 'Agda',
                                 'Android',
                                 'AppEngine',
                                 'AppceleratorTitanium',
                                 'ArchLinuxPackages',
                                 'Autotools',
                                 'C++',
                                 'C',
                                 'CFWheels',
                                 'CMake',
                                 'CONTRIBUTING.md',
                                 'CUDA',
                                 'CakePHP',
                                 'ChefCookbook',
                                 'Clojure',
                                 'CodeIgniter',
                                 'CommonLisp',
                                 'Composer',
                                 'Concrete5',
                                 'Coq',
                                 'CraftCMS',
                                 'D',
                                 'DM',
                                 'Dart',
                                 'Delphi',
                                 'Drupal',
                                 'EPiServer',
                                 'Eagle',
                                 'Elisp',
                                 'Elixir',
                                 'Elm',
                                 'Erlang',
                                 'ExpressionEngine',
                                 'ExtJs',
                                 'Fancy',
                                 'Finale',
                                 'FlaxEngine',
                                 'ForceDotCom',
                                 'Fortran',
                                 'FuelPHP',
                                 'GWT',
                                 'Gcov',
                                 'GitBook',
                                 'Go',
                                 'Godot',
                                 'Gradle',
                                 'Grails',
                                 'Haskell',
                                 'IGORPro',
                                 'Idris',
                                 'JBoss',
                                 'JENKINS_HOME',
                                 'Java',
                                 'Jekyll',
                                 'Joomla',
                                 'Julia',
                                 'KiCad',
                                 'Kohana',
                                 'Kotlin',
                                 'LICENSE',
                                 'LabVIEW',
                                 'Laravel',
                                 'Leiningen',
                                 'LemonStand',
                                 'Lilypond',
                                 'Lithium',
                                 'Lua',
                                 'Magento',
                                 'Maven',
                                 'Mercury',
                                 'MetaProgrammingSystem',
                                 'Nanoc',
                                 'Nim',
                                 'Node',
                                 'OCaml',
                                 'Objective-C',
                                 'Opa',
                                 'OpenCart',
                                 'OracleForms',
                                 'Packer',
                                 'Perl',
                                 'Phalcon',
                                 'PlayFramework',
                                 'Plone',
                                 'Prestashop',
                                 'Processing',
                                 'PureScript',
                                 'Python',
                                 'Qooxdoo',
                                 'Qt',
                                 'R',
                                 'README.md',
                                 'ROS',
                                 'Rails',
                                 'Raku',
                                 'RhodesRhomobile',
                                 'Ruby',
                                 'Rust',
                                 'SCons',
                                 'Sass',
                                 'Scala',
                                 'Scheme',
                                 'Scrivener',
                                 'Sdcc',
                                 'SeamGen',
                                 'SketchUp',
                                 'Smalltalk',
                                 'Stella',
                                 'SugarCRM',
                                 'Swift',
                                 'Symfony',
                                 'SymphonyCMS',
                                 'TeX',
                                 "Terraform",
                                 'Textpattern',
                                 'TurboGears2',
                                 'TwinCAT3',
                                 'Typo3',
                                 'Unity',
                                 'UnrealEngine',
                                 'VVVV',
                                 'VisualStudio',
                                 'Waf',
                                 'WordPress',
                                 'Xojo',
                                 'Yeoman',
                                 'Yii',
                                 'ZendFramework',
                                 'Zephir']

    valid_licenses = ["afl-3.0",
                      "apache-2.0",
                      "artistic-2.0",
                      "bsl-1.0",
                      "bsd-2-clause",
                      "bsd-3-clause",
                      "bsd-3-clause-clear",
                      "cc",
                      "cc0-1.0",
                      "cc-by-4.0",
                      "cc-by-sa-4.0",
                      "wtfpl",
                      "ecl-2.0",
                      "epl-1.0",
                      "epl-2.0",
                      "eupl-1.1",
                      "agpl-3.0",
                      "gpl",
                      "gpl-2.0",
                      "gpl-3.0",
                      "lgpl",
                      "lgpl-2.1",
                      "lgpl-3.0",
                      "isc",
                      "lppl-1.3c",
                      "ms-pl",
                      "mit",
                      "mpl-2.0",
                      "osl-3.0",
                      "postgresql",
                      "ofl-1.1",
                      "ncsa",
                      "unlicense",
                      "zlib"]

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    output_repo = {}

    if module.params['state'] not in valid_states:
        error_message = 'Invalid state: ' + module.params['state']
        module.exit_json(changed=False, err=error_message, failed=True)

    if module.params['api_url'] == '':
        g = Github(module.params['access_token'])
    else:
        g = Github(module.params['access_token'],
                   base_url=module.params['api_url'])

    try:
        repo = g.get_organization(
            module.params['organization']).get_repo(module.params['repository_name'])
        initial = {
            "name": repo.name,
            "full_name": repo.full_name,
            "owner": repo.owner.login,
            "description": repo.description,
            "private": repo.private,
            "archived": repo.archived,
            "language": repo.language,
            "url": repo.url,
            "default_branch": repo.default_branch,
            "hooks_url": repo.hooks_url,
            "clone_url": repo.clone_url,
            "allow_merge_commit": repo.allow_merge_commit,
            "allow_rebase_merge": repo.allow_rebase_merge,
            "allow_squash_merge": repo.allow_squash_merge,
            "delete_branch_on_merge": repo.delete_branch_on_merge,
            "has_issues": repo.has_issues,
            "has_downloads": repo.has_downloads,
            "has_wiki": repo.has_wiki,
            "has_projects": repo.has_projects,
            "homepage": repo.homepage
        }
    except Exception as e:
        initial = {}

    if module.params['state'] == 'present':
        try:
            if module.params['license_template'] and module.params['license_template'] not in valid_licenses:
                error_message = 'Invalid license: ' + \
                    module.params['license_template']
                module.exit_json(changed=False, err=error_message, failed=True)

            if module.params['gitignore_template'] and module.params['gitignore_template'] not in valid_gitignore_templates:
                error_message = 'Invalid gitignore template: ' + \
                    module.params['gitignore_template']
                module.exit_json(changed=False, err=error_message, failed=True)
            repo = g.get_organization(module.params['organization']).get_repo(
                module.params['repository_name'])
            if repo:
                if module.check_mode:
                    output_repo = repo
                    output_repo.private = module.params["private"]
                    output_repo.description = module.params["description"]
                    output_repo.homepage = module.params["homepage"]
                    output_repo.has_issues = module.params["has_issues"]
                    output_repo.has_wiki = module.params["has_wiki"]
                    output_repo.has_downloads = module.params["has_downloads"]
                    output_repo.has_projects = module.params["has_projects"]
                    output_repo.allow_merge_commit = module.params["allow_merge_commit"]
                    output_repo.allow_rebase_merge = module.params["allow_rebase_merge"]
                    output_repo.allow_squash_merge = module.params["allow_squash_merge"]
                    output_repo.delete_branch_on_merge = module.params["delete_branch_on_merge"]
                else:
                    repo.edit(name=module.params['repository_name'],
                              description=module.params['description'],
                              homepage=module.params['homepage'],
                              private=module.params['private'],
                              has_issues=module.params['has_issues'],
                              has_projects=module.params['has_projects'],
                              has_wiki=module.params['has_wiki'],
                              has_downloads=module.params['has_downloads'],
                              allow_squash_merge=module.params['allow_squash_merge'],
                              allow_merge_commit=module.params['allow_merge_commit'],
                              allow_rebase_merge=module.params['allow_rebase_merge'],
                              delete_branch_on_merge=module.params['delete_branch_on_merge'])
        except Exception as e:
            org = g.get_organization(module.params['organization'])
            for team in org.get_teams():
                if team.name == module.params['team_name']:
                    if module.check_mode:
                        if module.params['api_url']:
                            noApiurl = str(module.params['api_url']).replace(
                                "/api/v3", "")
                            clone_url = "%s/%s/%s.git" % (
                                noApiurl, module.params['organization'], module.params['repository_name'])
                            url = "%s/repos/%s/%s" % (
                                module.params['api_url'], module.params['organization_name'], module.params['repository_name'])
                            hooks_url = "%s/hooks" % (url)
                        else:
                            clone_url = "https://github.com/%s/%s.git" % (
                                module.params['organization_name'], module.params['repository_name'])
                            url = "https://github.com/api/v3/repos/%s/%s" % (
                                module.params['enterprise_url'], module.params['organization'], module.params['repository_name'])
                            hooks_url = "%s/hooks" % (url)
                        full_name = "%s/%s" % (
                            module.params['organization'], module.params['repository_name'])
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
                            "name": module.params['repo_name'],
                            "owner": module.params['organization_name'],
                            "private": module.params['private'],
                            "url": url
                        }
                    else:
                        g.get_organization(module.params['organization']).create_repo(
                            module.params['repository_name'],
                            module.params['description'],
                            module.params['homepage'],
                            module.params['private'],
                            module.params['has_issues'],
                            module.params['has_wiki'],
                            module.params['has_downloads'],
                            module.params['has_projects'],
                            team.id,
                            module.params['auto_init'],
                            module.params['license_template'],
                            module.params['gitignore_template'],
                            module.params['allow_squash_merge'],
                            module.params['allow_merge_commit'],
                            module.params['allow_rebase_merge'],
                            module.params['delete_branch_on_merge']
                        )
    else:
        try:
            if not module.check_mode:
                repo = g.get_organization(module.params['organization']).get_repo(
                    module.params['repository_name']).delete()

        except Exception as e:
            ...

    try:
        repo = g.get_organization(
            module.params['organization']).get_repo(module.params['repository_name'])
        output = {
            "name": repo.name,
            "full_name": repo.full_name,
            "owner": repo.owner.login,
            "description": repo.description,
            "private": repo.private,
            "archived": repo.archived,
            "language": repo.language,
            "url": repo.url,
            "default_branch": repo.default_branch,
            "hooks_url": repo.hooks_url,
            "clone_url": repo.clone_url,
            "allow_merge_commit": repo.allow_merge_commit,
            "allow_rebase_merge": repo.allow_rebase_merge,
            "allow_squash_merge": repo.allow_squash_merge,
            "delete_branch_on_merge": repo.delete_branch_on_merge,
            "has_issues": repo.has_issues,
            "has_downloads": repo.has_downloads,
            "has_wiki": repo.has_wiki,
            "has_projects": repo.has_projects,
            "homepage": repo.homepage
        }
    except Exception as e:
        output = {}

    if module.check_mode:
        module.exit_json(repo=output_repo, changed=initial != output_repo)
    else:
        module.exit_json(repo=output, changed=initial != output)


def main():
    run_module()


if __name__ == '__main__':
    main()
